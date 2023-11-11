# importing the requests library
import requests
from utils.log import debug, info, error, log

class juicy():

    def __init__(self):
        self.key = '8f4f7ccd11b3bcbafbffff1212db142d'
        self.order_number = None
        self.phone_number = None
        self.code = None
        self.area = 'USA'


    def get_balance(self):
        request = f'https://juicysms.com/api/getbalance?key={self.key}'
        response = requests.get(request)
        debug(response.text)
    

    def get_number_from_order(self, order_number):
        return '07774403727'
        raise Exception("Not implemented") 
        pass
        # request = f'https://juicysms.com/api/getnumber?key={self.key}&order={order_number}'
        # response = requests.get(request)
        # debug(response.text)
        # return response.text

    def reuse_number(self):
        pass

    def get_code(self):
        request = f'https://juicysms.com/api/getsms?key={self.key}&orderId={self.order_number}'
        response = requests.get(request)
        debug(response.text)
        if 'ORDER_EXPIRED' in response.text:
            raise Exception("Order expired")

        if 'WAITING' in response.text:
            return -1

        debug(self.code)
        self.code = response.text.split('_')[-1]
        return self.code

    def get_number(self):
        if self.phone_number != None:
            try: 
                number = self.reuse_number()
                return number
            except:
                log(f"Phone number {self.phone_number} is not available for reuse")

        debug("Trying US")
        request = f'https://juicysms.com/api/makeorder?key={self.key}&serviceId=1&country={self.area}'
        response = requests.get(request)
        debug(response.text)

        if response.text == 'NO_PHONE_AVAILABLE':
            debug("Trying UK")
            self.area = 'UK'
            request = f'https://juicysms.com/api/makeorder?key={self.key}&serviceId=1&country={self.area}'
            response = requests.get(request)
            debug(response.text)

            if response.text == 'NO_PHONE_AVAILABLE':
                debug("Trying NL")
                self.area = 'NL'
                request = f'https://juicysms.com/api/makeorder?key={self.key}&serviceId=1&country={self.area}'
                response = requests.get(request)
                debug(response.text)

                if response.text == 'NO_PHONE_AVAILABLE':
                        log("No phone number available")
                        raise Exception("No phone number available")
        
        if 'ORDER_ALREADY_OPEN_' in response.text:
            self.order_number = response.text.split('_')[-1]
            self.phone_number = self.get_number_from_order(self.order_number)
            return self.area, self.phone_number
        
        if 'NO_BALANCE' in response.text:
            raise Exception("No balance")

        self.order_number = response.text.split('_')[1]
        self.phone_number = response.text.split('_')[-1]

        return self.area, self.phone_number