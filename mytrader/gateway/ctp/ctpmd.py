# 导入ctp市场行情接口
from mytrader.gateway.ctp.lib import thostmduserapi
from mytrader.event import Event, EventType, EventEngine


APP_NAME = 'MarketDataEngine'

USER_ID = '151650'  # 用户名
PASSWORD = '88200927'  # 密码
BROKER_ID = '8000'  # 代理号码
FRONT_ADDR = 'tcp://180.168.146.187:10131'  # 服务器地址


SUB_SYMBOL = set(['SR005', 'i2005'])  # 订阅的合约集合

# 连接中断的原因
DISCONNECT_REASON = {
    0x1001: "网络读失败",
    0x1002: "网络写失败",
    0x2001: "接收心跳超时",
    0x2002: "发送心跳失败",
    0x2003: "收到错误报文",
}

# 事件类型
E_MD_CONNECTED = EventType('eMdConnected')  # 与行情服务器连接成功
E_MD_DISCONNECTED = EventType('eMdDisconnected')  # 与行情服务器连接断开
E_MD_LOGIN = EventType('eMdLogin') # 在行情服务器上登录
E_MD_SUBMARKETDATA = EventType('eMdSubMarketData')  # 订阅行情数据
E_MD_TICK = EventType('eMdTick')    # Tick数据到来


def is_rsp_error(error_id: int):
    """判断回复信息是否错误"""
    if error_id == 0:  # 一般来说0表示正确
        return False
    else:
        return True


class CtpMdSpi(thostmduserapi.CThostFtdcMdSpi):
    """
    行情回调接口
    """
    def __init__(self, event_engine: EventEngine):
        thostmduserapi.CThostFtdcMdSpi.__init__(self)
        # 事件引擎
        self.event_engine = event_engine

    def OnFrontConnected(self):
        """如果连接上行情服务器，即建立起TCP连接"""
        # 发送一个连接成功的事件
        event = Event(E_MD_CONNECTED, None)
        self.event_engine.put(event)

    def OnFrontDisconnected(self, nReason: 'int'):
        """与服务器连接断开"""
        # 发送一个连接失败的事件
        data = {
            "error_id": nReason,  # 错误代码
            "error_msg": DISCONNECT_REASON[nReason],  # 错误信息
        }
        event = Event(E_MD_DISCONNECTED, data)
        self.event_engine.put(event)

    def OnRspUserLogin(self, pRspUserLogin: 'CThostFtdcRspUserLoginField', pRspInfo: 'CThostFtdcRspInfoField',
                       nRequestID: 'int', bIsLast: 'bool'):
        """请求登录的回调函数"""
        # 构建事件数据
        data = {
            "user_id": pRspUserLogin.UserID,   # 登录用户名
            "login_time": pRspUserLogin.LoginTime,  # 登录时间
            "error_id": pRspInfo.ErrorID,   # 登录错误标识
            "error_msg": pRspInfo.ErrorMsg, # 登录错误信息
            "request_id": nRequestID,   # 请求序列号
            "is_last": bIsLast, # 最近标识符，按文档说无用
        }
        # 发送一个登录事件
        event = Event(E_MD_LOGIN, data)
        self.event_engine.put(event)

    def OnRspSubMarketData(self, pSpecificInstrument: 'CThostFtdcSpecificInstrumentField',
                           pRspInfo: 'CThostFtdcRspInfoField', nRequestID: 'int', bIsLast: 'bool'):
        """订阅合约行数数据请求的回调函数"""
        # 构建事件数据
        data = {
            "symbol": pSpecificInstrument.InstrumentID,    # 合约号
            "error_id": pRspInfo.ErrorID,   # 登录错误标识
            "error_msg": pRspInfo.ErrorMsg, # 登录错误信息
            "request_id": nRequestID,   # 请求序列号
            "is_last": bIsLast,
        }
        # 发送一个订阅合约行情回复事件
        event = Event(E_MD_SUBMARKETDATA, data)
        self.event_engine.put(event)

    def OnRtnDepthMarketData(self, pDepthMarketData: 'CThostFtdcDepthMarketDataField'):
        """当有新的行情数据到达时的回调函数"""
        # 在这里组织Tick数据
        # 发送一个Tick数据到达事件
        event = Event(E_MD_TICK, None)
        self.event_engine.put(event)
        print(f"交易日:{pDepthMarketData.TradingDay}, 合约号:{pDepthMarketData.InstrumentID},"
              f"最新价:{pDepthMarketData.LastPrice}, 手数:{pDepthMarketData.Volume}"
              f"最高价:{pDepthMarketData.HighestPrice}, 最低价:{pDepthMarketData.LowestPrice}"
              f"开盘价:{pDepthMarketData.OpenPrice}, 收盘价:{pDepthMarketData.ClosePrice}")


class MarketDataEngine(object):
    """行情数据引擎"""
    def __init__(self, event_engine: EventEngine, engine_name: str = APP_NAME):
        # 设置事件引擎
        self.event_engine = event_engine
        # 设置引擎名称
        self.engine_name = engine_name

        # 引擎是否运行标识符
        self.__active = False
        # 记录当前的请求序列号
        self.__request_id = -1
        # 是否与行情服务器连接标识符
        self.__is_connect = False
        # 是否登录成功标识符
        self.__is_login = False

        # 行情数据接口
        self.api = None
        # 行情数据回调接口
        self.spi = None

        # 注册事件
        self.register_event()

    @property
    def request_id(self):
        """得到请求序列号"""
        self.__request_id += 1  # 请求序号递增
        return self.__request_id

    def init_variable(self):
        # 引擎是否运行标识符
        self.__active = False
        # 记录当前的请求序列号
        self.__request_id = -1
        # 是否与行情服务器连接标识符
        self.__is_connect = False
        # 是否登录成功标识符
        self.__is_login = False

        # 行情数据接口
        self.api = None
        # 行情数据回调接口
        self.spi = None

    def register_event(self):
        """注册事件"""
        # 注册行情服务器连接成功事件
        self.event_engine.register(E_MD_CONNECTED, self.__on_connected)
        # 注册行情服务器连接失败事件
        self.event_engine.register(E_MD_DISCONNECTED, self.__on_disconnected)
        # 注册登录事件
        self.event_engine.register(E_MD_LOGIN, self.__on_login)
        # 注册合约行情数据订阅事件
        self.event_engine.register(E_MD_SUBMARKETDATA, self.__on_submarketdata)

    def __on_connected(self, event: Event):
        """与行情服务器连接成功的处理方法"""
        self.__is_connect = True
        print("连接行情服务器成功")
        # 连接成功，自动登录
        self.login()

    def __on_disconnected(self, event: Event):
        """与行情服务器连接中断的处理方法"""
        self.__is_connect = False
        self.__is_login = False
        # 获取中断原因
        data = event.data
        print(f"与行情服务器连接中断，错误代码:{data['error_id']}, 错误原因:{data['error_msg']}")

    def __on_login(self, event: Event):
        """登录事件的处理方法"""
        # 获取事件数据
        data = event.data
        # 如果登录错误
        if is_rsp_error(data["error_id"]):
            print(f"登录失败，错误代码:{data['error_id']}，错误原因:{data['error_msg']}")
        # 如果登录成功
        else:
            print(f"登录成功，用户名:{data['user_id']}, 登录时间:{data['login_time']}")
            # 设置登录成功标识
            self.__is_login = True
            # 自动订阅合约行情数据
            for symbol in SUB_SYMBOL:
                self.subscribe(symbol)

    def __on_submarketdata(self, event: Event):
        """订阅行情数据的处理方法"""
        # 获取事件数据
        data = event.data
        # 如果订阅失败
        if is_rsp_error(data['error_id']):
            print(f"订阅合约 {data['symbol']} 失败，错误代码：{data['error_id']}，错误原因：{data['error_msg']}")
        else:
            print(f"订阅合约 {data['symbol']} 成功")

    def login(self):
        """登录方法"""
        # 判断是否成功连接到服务器
        if not self.__is_connect:
            print("无法登录：未连接到服务器")
            return
        # 构建登录信息
        login_field = thostmduserapi.CThostFtdcReqUserLoginField()
        login_field.UserID = USER_ID
        login_field.Password = PASSWORD
        login_field.BrokerID = BROKER_ID
        login_field.UserProductInfo = "python dll"
        # 调用接口发送登录请求
        ret = self.api.ReqUserLogin(login_field, self.request_id)
        print("正在登录....")
        return ret

    def logout(self):
        """登出方法"""
        # 登出信息
        logout_field = thostmduserapi.CThostFtdcUserLogoutField()
        logout_field.UserID = USER_ID
        logout_field.BrokerID = BROKER_ID
        # 调用接口发送登出请求
        ret = self.api.ReqUserLogout(logout_field, self.request_id)
        return ret

    def subscribe(self, symbol: str):
        """订阅合约的行情数据"""
        # 如果未登录
        if not self.__is_login:
            print("请先登录")
            return
        # 调用接口订阅函数
        ret = self.api.SubscribeMarketData([symbol.encode("utf-8")], 1)
        print(f"正在订阅合约 {symbol}")
        return ret

    def unsubsribe(self, symbol):
        """取消订阅行情数据"""
        ret = self.api.UnSubscribeMarketData([symbol.encode("utf-8")], 1)
        print(f"正在取消订阅合约{symbol}")
        return ret

    def start(self):
        """引擎启动方法"""
        # 先调用一次引擎停止方法，确保引擎处在关闭状态
        self.stop()
        # 创建行情数据接口实例
        self.api = thostmduserapi.CThostFtdcMdApi_CreateFtdcMdApi()
        # 设置行情服务器地址
        self.api.RegisterFront(FRONT_ADDR)
        # 创建行情数据回调实例
        self.spi = CtpMdSpi(self.event_engine)
        # 注册回调类
        self.api.RegisterSpi(self.spi)
        # 初始化接口对象
        self.api.Init()
        # 设置引擎运行标识
        self.__active = True

    def stop(self):
        """引擎关闭方法"""
        if self.api:
            # 登出行情服务器
            self.logout()
            # 释放api线程
            self.api.Release()
        # 重置所有值
        self.init_variable()
