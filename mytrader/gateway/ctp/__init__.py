"""
    此CTP Python API基于Python 3.7.2版本，使用时请务必安装此版本及以上版本。
    该API是用swig方法在官方C++ API上编译得到。
    CTP API官网：http://www.sfit.com.cn/

    CTP的API封装分为两大部分:
    （1）MdUserApi(thostmduserapi.py)接口：负责行情订阅
        通过CThostFtdcMdApi下命令，通过CThostFtdcMdSpi来响应命令的回调
    （2）TraderApi(thosttraderapi.py):负责交易，包括确认结算结果、查询合约、查询资金、查询持仓、报单、收委托回报、撤单
        通过CThostFtdcTraderApi向CTP发送操作请求，通过CThostFtdcTraderSpi接收CTP的操作响应

    使用方式：
    继承接口类，并重写相关方法即可

    常见指标的含义：
    （1）nRequestID：发送请求时需指定<请求号>，因为TradeApi是异步实现，<请求号>可以把请求/查询指令和相关回报关联起来
    （2）IsLast：无论是否有查询响应数据，只要查询响应结束，IsLast为True
    （3）响应信息RspInfo
        - 如果RspInfo为空，或RspInfo的错误代码为空，说明查询成功
        - 否则RspInfo中会保存错误编码和错误信息

    API命名规则：
    |消息|格式|示例|
    |---|---|---|
    |请求|Req..|ReqUserLogin|
    |响应|OnRsp..|OnRspUserLogin|
    |查询|ReqQry..|ReqQryInstrument|
    |查询请求的响应|OnRspQry..|OnRspQryInstrument|
    |回报|OnRtn..|OnRtnOrder|
    |错误回报|OnErrRtn..|OnErrRtnOrderInsert|

    断开连接: OnFrontDisconnected
        - 0x1001：网络读失败
        - 0x1002：网络写失败
        - 0x2001：接收心跳超时
        - 0x2002：发送心跳失败
        - 0x2003：收到错误报文

    确认结算：ReqSettlementInfoConfirm OnRspSettlementInfoConfirm
        当日首次登录必须确认结算
    查询当日有无结算：ReqQrySettlementInfoConfirm OnRspSettlementInfoConfirm
    查询结算信息：ReqQrySettlementInfo OnRspQrySettlementInfoConfirm

    查合约：ReqQryInstrument OnRspQryInstrument

    登出：ReqUserLogout OnRspUserLogout

    订阅市场数据：SubscribeMarketData  OnRspSubMarketData OnRtnDepthMarketData

    报单：ReqOrderInsert OnRspOrderInsert OnErrRtnOrderInsert OnRtnOrder OnRtnTrade
    报单标识：
        - FrontID + SessionID + OrderRef (注意OrderRef长度,为int atoi)
        - BrokerID + BrokerOrderSeq
        - ExchangeID + OrderSysID

    撤单：ReqOrderAction OnRspOrderAction OnErrRtnOrderAction OnRtnOrder

    查持仓：ReqQryInvestorPosition OnRspQryInvestorPosition ReqQryInvestorPositionDetail OnRspQryInvestorPositionDetail

    查资金：ReqQryTradingAccount OnRspQryTradingAccount
        - 静态权益 = 上日结算 - 出金金额 + 入金金额 （account.PreBalance - account.Withdraw + account.Deposit）
        - 动态权益 = 静态权益 + 平仓盈亏 + 持仓盈亏 - 手续费
            静态权益 + account.CloseProfit + account.PositionProfit - account.Commission
        - 可用资金 = 动态权益 - 占用保证金 - 冻结保证金 - 冻结手续费 - 交割保证金
            account.Available

    查手续费：ReqQryInstrumentCommissionRate OnRspQryInstrumentCommissionRate
        按合约查询，以品种响应


"""