import os
import secrets
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
    
    
    SECRET_KEY=os.environ.get('SECRET_KEY')
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('USERNAME')
    APP_ADMIN=os.environ.get('USERNAME')
    MAIL_PASSWORD=os.environ.get('PASSWORD')
    CONSUMER_KEY=os.environ.get('Consumer_Key')
    CONSUMER_SECRET=os.environ.get('Consumer_Secret')
    
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
