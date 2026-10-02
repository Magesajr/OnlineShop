import os
from datetime import timedelta


base=os.path.abspath(os.path.dirname(__file__))

class config:
    #live creditials    
    PESAPAL_AUTH='https://pay.pesapal.com/v3/api/Auth/RequestToken'
    PESAPAL_REG='https://pay.pesapal.com/v3/api/URLSetup/RegisterIPN'
    PESAPAL_SUBMIT='https://pay.pesapal.com/v3/api/Transactions/SubmitOrderRequest'
    PESAPAL_ORDER_CANCEL='https://pay.pesapal.com/v3/api/Transactions/CancelOrder'
    PESAPAL_REFUND='https://pay.pesapal.com/v3/api/Transactions/RefundRequest'
    PESAPAL_ORDER_TRACK='https://pay.pesapal.com/v3/api/Transactions/GetTransactionStatus?orderTrackingId='
    IPN='c6a79787-8bb3-4f2a-9f99-dbf9a382388f'

    #test creditials 
    PESAPAL_AUTH_DEMO='https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken'
    PESAPAL_REG_DEMO='https://cybqa.pesapal.com/pesapalv3/api/URLSetup/RegisterIPN'
    PESAPAL_SUBMIT_DEMO='https://cybqa.pesapal.com/pesapalv3/api/Transactions/SubmitOrderRequest'
    PESAPAL_ORDER_CANCEL_DEMO='https://cybqa.pesapal.com/pesapalv3/api/Transactions/CancelOrder'
    PESAPAL_REFUND_DEMO='https://cybqa.pesapal.com/pesapalv3/api/Transactions/RefundRequest'
    PESAPAL_ORDER_TRACK_DEMO='https://cybqa.pesapal.com/pesapalv3/api/Transactions/GetTransactionStatus?orderTrackingId='
    IPN_DEMO='a68237b3-cf86-4902-8213-dbf9e39e6de5'

    CONSUMER_KEY_DEMO='ngW+UEcnDhltUc5fxPfrCD987xMh3Lx8'
    CONSUMER_SECRET_DEMO='q27RChYs5UkypdcNYKzuUw460Dg='


    #LIPAHURU  LIVE CREDENTIALS
    LIPA_BASE='https://pgw.lipahuru.co.tz'
    LIPA_TOKEN='/oauth/token'
    LIPA_COLLECT='/api/v1/payments/collections/push'
    LIPA_STATUS=f'/api/v1/payments/'
    LIPA_MINE='/api/v1/payments/disbursements'
    LIPA_QUERY='/api/v1/payments/'
    LIPA_BALANCE='api/v1/wallets/YAS'
    CLIENT_ID= os.environ.get('CLIENT_ID')
    CLIENT_SECRET=os.environ.get('CLIENT_SECRET') 
    PAYMENT_FEE=1000
    
    #auths
    SECRET_KEY=os.environ.get('SECRET_KEY')
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('USERNAME')
    APP_ADMINS=os.environ.get('APP_ADMINS','').split(':')
    MAIL_PASSWORD=os.environ.get('PASSWORD')
    CONSUMER_KEY=os.environ.get('Consumer_Key')
    CONSUMER_SECRET=os.environ.get('Consumer_Secret')
    SUPABASE_URL='https://xypiifoukifsdpuhcguw.supabase.co'
    SUPABASE_KEY = os.environ.get('SUPA_KEY')
    #sessions
    PERMANENT_SESSION_LIFETIME=timedelta(days=1)
    SESSION_REFRESH_EACH_REQUEST=False
    REMEMBER_COOKIE=timedelta(days=1)

    @staticmethod
    def init_app(app):
        pass

class Development(config):
    DEBUG=True
    Database=base+'/DATABASE'
    Upload=base+'/UPLOAD'
    if  not os.path.exists(Database):
        os.makedirs(Database)
    if  not os.path.exists(Upload):
        os.makedirs(Upload)
    database=os.path.join(base,Database+'/database.sqlite')
    SQLALCHEMY_DATABASE_URI='sqlite:///' + database
    UPLOAD_FOLDER=Upload


class Production(config):
    SQLALCHEMY_DATABASE_URI=os.environ.get('SUPABASE_POSTGRES')


conf={
    'default':Development,
    'production':Production
}
