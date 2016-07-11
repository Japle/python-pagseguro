# coding: utf-8
import logging
import requests
import xmltodict

from .configs import Config, ConfigSandbox, AbstractConfig  # noqa
from .utils import parse_date, is_valid_email, is_valid_cpf, is_valid_cnpj

logger = logging.getLogger()


class PagSeguroNotificationResponse(object):

    def __init__(self, xml, config=None):
        self.xml = xml
        self.config = config or {}
        self.errors = None
        self.parse_xml(xml)

    def __getitem__(self, key):
        getattr(self, key, None)

    def parse_xml(self, xml):
        try:
            parsed = xmltodict.parse(xml, encoding="iso-8859-1")
        except Exception as e:
            logger.debug(
                "Cannot parse the returned xml '{0}' -> '{1}'".format(xml, e))
            parsed = {}

        if 'errors' in parsed:
            self.errors = parsed['errors']['error']
            return

        transaction = parsed.get('transaction', {})
        for k, v in transaction.items():
            setattr(self, k, v)


class PagSeguroPreApprovalNotificationResponse(object):

    def __init__(self, xml, config=None):
        self.xml = xml
        self.config = config or {}
        self.errors = None
        self.parse_xml(xml)

    def __getitem__(self, key):
        getattr(self, key, None)

    def parse_xml(self, xml):
        try:
            parsed = xmltodict.parse(xml, encoding="iso-8859-1")
        except Exception as e:
            logger.debug(
                "Cannot parse the returned xml '{0}' -> '{1}'".format(xml, e))
            parsed = {}

        if 'errors' in parsed:
            self.errors = parsed['errors']['error']
            return

        transaction = parsed.get('preApproval', {})
        for k, v in transaction.items():
            setattr(self, k, v)


class PagSeguroPreApprovalCancel(object):

    def __init__(self, xml, config=None):
        self.xml = xml
        self.config = config or {}
        self.errors = None
        self.parse_xml(xml)

    def __getitem__(self, key):
        getattr(self, key, None)

    def parse_xml(self, xml):
        try:
            parsed = xmltodict.parse(xml, encoding="iso-8859-1")
        except Exception as e:
            logger.debug(
                "Cannot parse the returned xml '{0}' -> '{1}'".format(xml, e))
            parsed = {}

        if 'errors' in parsed:
            self.errors = parsed['errors']['error']
            return

        transaction = parsed.get('result', {})
        for k, v in transaction.items():
            setattr(self, k, v)


class PagSeguroCheckoutSession(object):

    def __init__(self, xml, config=None):
        self.xml = xml
        self.config = config or {}
        self.session_id = None
        self.errors = None
        logger.debug(self.__dict__)
        self.parse_xml(xml)

    def parse_xml(self, xml):
        """ parse returned data """

        try:
            parsed = xmltodict.parse(xml, encoding="iso-8859-1")
        except Exception as e:
            logger.debug(
                "Cannot parse the returned xml '{0}' -> '{1}'".format(xml, e))
            parsed = {}

        if 'errors' in parsed:
            self.errors = parsed['errors']['error']
            return

        session = parsed.get('session', {})
        self.session_id = session.get('id')


class PagSeguroPreApprovalPayment(object):
    def __init__(self, xml, config=None):
        self.xml = xml
        self.config = config or {}
        self.code = None
        self.errors = None
        logger.debug(self.__dict__)
        self.parse_xml(xml)

    def parse_xml(self, xml):
        """ parse returned data """
        try:
            parsed = xmltodict.parse(xml, encoding="iso-8859-1")
        except Exception as e:
            logger.debug(
                "Cannot parse the returned xml '{0}' -> '{1}'".format(xml, e))
            parsed = {}

        if 'errors' in parsed:
            self.errors = parsed['errors']['error']
            return

        result = parsed.get('result', {})
        self.code = result.get('transactionCode')
        self.date = parse_date(result.get('date'))


class PagSeguroCheckoutResponse(object):

    def __init__(self, xml, config=None):
        self.xml = xml
        self.config = config or {}
        self.code = None
        self.date = None
        self.errors = None
        self.payment_url = None
        self.payment_link = None
        self.transaction = None
        logger.debug(self.__dict__)
        self.parse_xml(xml)

    def parse_xml(self, xml):
        """ parse returned data """
        try:
            parsed = xmltodict.parse(xml, encoding="iso-8859-1")
        except Exception as e:
            logger.debug(
                "Cannot parse the returned xml '{0}' -> '{1}'".format(xml, e))
            parsed = {}

        if 'errors' in parsed:
            self.errors = parsed['errors']['error']
            return

        checkout = parsed.get('checkout', {})
        self.code = checkout.get('code')
        self.date = parse_date(checkout.get('date'))

        self.payment_url = self.config.PAYMENT_URL % self.code

        # this is used only for transparent checkout process

        self.transaction = parsed.get('transaction', {})
        self.payment_link = self.transaction.get('paymentLink')


class PagSeguroTransactionSearchResult(object):

    current_page = None
    total_pages = None
    results_in_page = None
    transactions = []

    def __init__(self, xml, config=None):
        self.xml = xml
        self.config = config or {}
        self.parse_xml(xml)

    def __getitem__(self, key):
        getattr(self, key, None)

    def parse_xml(self, xml):
        try:
            parsed = xmltodict.parse(xml, encoding="iso-8859-1")
        except Exception as e:
            logger.debug(
                "Cannot parse the returned xml '{0}' -> '{1}'".format(xml, e))
            parsed = {}

        search_result = parsed.get('transactionSearchResult', {})
        self.transactions = search_result.get('transactions', {})
        self.transactions = self.transactions.get('transaction', [])
        if not isinstance(self.transactions, list):
            self.transactions = [self.transactions]
        self.current_page = search_result.get('currentPage', None)
        if self.current_page is not None:
            self.current_page = int(self.current_page)
        self.results_in_page = search_result.get('resultsInThisPage', None)
        if self.results_in_page is not None:
            self.results_in_page = int(self.results_in_page)
        self.total_pages = search_result.get('totalPages', None)
        if self.total_pages is not None:
            self.total_pages = int(self.total_pages)


class PagSeguroPreApproval(object):

    def __init__(self, xml, config=None):
        self.xml = xml
        self.config = config or {}
        self.errors = None
        self.parse_xml(xml)

    def __getitem__(self, key):
        getattr(self, key, None)

    def parse_xml(self, xml):
        try:
            parsed = xmltodict.parse(xml, encoding="iso-8859-1")
        except Exception as e:
            logger.debug(
                "Cannot parse the returned xml '{0}' -> '{1}'".format(xml, e)
            )
            parsed = {}

        result = parsed.get('preApproval', {})
        self.name = result.get('name', None)
        self.code = result.get('code', None)
        self.date = parse_date(result.get('date'))
        self.tracker = result.get('tracker', None)
        self.status = result.get('status', None)
        self.reference = result.get('reference', None)
        self.last_event_date = result.get('lastEventDate', None)
        self.charge = result.get('charge', None)
        self.sender = result.get('sender', {})


class PagSeguroPreApprovalSearch(object):

    current_page = None
    total_pages = None
    results_in_page = None
    pre_approvals = []

    def __init__(self, xml, config=None):
        self.xml = xml
        self.config = config or {}
        self.errors = None
        self.parse_xml(xml)

    def __getitem__(self, key):
        getattr(self, key, None)

    def parse_xml(self, xml):
        try:
            parsed = xmltodict.parse(xml, encoding="iso-8859-1")
        except Exception as e:
            logger.debug(
                "Cannot parse the returned xml '{0}' -> '{1}'".format(xml, e))
            parsed = {}

        if 'errors' in parsed:
            self.errors = parsed['errors']['error']
            return

        search_result = parsed.get('preApprovalSearchResult', {})
        self.pre_approvals = search_result.get('preApprovals', {})
        self.pre_approvals = self.pre_approvals.get('preApproval', [])
        if not isinstance(self.pre_approvals, list):
            self.pre_approvals = [self.pre_approvals]
        self.current_page = search_result.get('currentPage', None)
        if self.current_page is not None:
            self.current_page = int(self.current_page)
        self.results_in_page = search_result.get('resultsInThisPage', None)
        if self.results_in_page is not None:
            self.results_in_page = int(self.results_in_page)
        self.total_pages = search_result.get('totalPages', None)
        if self.total_pages is not None:
            self.total_pages = int(self.total_pages)


class PagSeguro(object):
    """ Pag Seguro V2 wrapper """

    PAC = 1
    SEDEX = 2
    NONE = 3

    def __init__(self, email, token, data=None, config=None):

        self.config = config or Config()
        assert isinstance(self.config, AbstractConfig), \
            "Config should be instance of AbstractConfig"
        self.data = {}
        self.data['email'] = email
        self.data['token'] = token

        if data and isinstance(data, dict):
            self.data.update(data)

        self.items = []
        self.sender = {}
        self.shipping = {}
        self._reference = ""
        self.extra_amount = None
        self.redirect_url = None
        self.notification_url = None
        self.abandon_url = None
        self.credit_card = {}
        self.pre_approval = {}
        self.checkout_session = None
        self.payment = {}

    def build_checkout_params(self, **kwargs):
        """ build a dict with params """
        params = kwargs or {}
        if self.sender:
            params['senderName'] = self.sender.get('name')
            params['senderAreaCode'] = self.sender.get('area_code')
            params['senderPhone'] = self.sender.get('phone')
            params['senderEmail'] = is_valid_email(self.sender.get('email'))
            params['senderCPF'] = is_valid_cpf(self.sender.get('cpf'))
            params['senderCNPJ'] = is_valid_cnpj(self.sender.get('cnpj'))
            params['senderBornDate'] = self.sender.get('born_date')
            params['senderHash'] = self.sender.get('hash')

        if self.shipping:
            params['shippingType'] = self.shipping.get('type')
            params['shippingAddressStreet'] = self.shipping.get('street')
            params['shippingAddressNumber'] = self.shipping.get('number')
            params['shippingAddressComplement'] = self.shipping.get(
                'complement')
            params['shippingAddressDistrict'] = self.shipping.get('district')
            params['shippingAddressPostalCode'] = self.shipping.get(
                'postal_code')
            params['shippingAddressCity'] = self.shipping.get('city')
            params['shippingAddressState'] = self.shipping.get('state')
            params['shippingAddressCountry'] = self.shipping.get('country',
                                                                 'BRA')

        if self.shipping and self.shipping.get('cost'):
            params['shippingCost'] = self.shipping.get('cost')

        if self.extra_amount:
            params['extraAmount'] = self.extra_amount

        params['reference'] = self.reference
        params['receiverEmail'] = self.data['email']

        if self.redirect_url:
            params['redirectURL'] = self.redirect_url

        if self.notification_url:
            params['notificationURL'] = self.notification_url

        if self.abandon_url:
            params['abandonURL'] = self.abandon_url

        for i, item in enumerate(self.items, 1):
            params['itemId%s' % i] = item.get('id')
            params['itemDescription%s' % i] = item.get('description')
            params['itemAmount%s' % i] = item.get('amount')
            params['itemQuantity%s' % i] = item.get('quantity')
            params['itemWeight%s' % i] = item.get('weight')
            params['itemShippingCost%s' % i] = item.get('shipping_cost')

        if self.payment:

            params['paymentMethod'] = self.payment.get('method')
            params['paymentMode'] = self.payment.get('mode')

        if self.credit_card:
            params['billingAddressCountry'] = 'BRA'

            credit_card_keys_map = [
                ('creditCardToken', 'credit_card_token'),
                ('installmentQuantity', 'installment_quantity'),
                ('installmentValue', 'installment_value'),
                ('noInterestInstallmentQuantity',
                 'no_interest_installment_quantity'),
                ('creditCardHolderName', 'card_holder_name'),
                ('creditCardHolderCPF', 'card_holder_cpf'),
                ('creditCardHolderBirthDate', 'card_holder_birth_date'),
                ('creditCardHolderAreaCode', 'card_holder_area_code'),
                ('creditCardHolderPhone', 'card_holder_phone'),
                ('billingAddressStreet', 'billing_address_street'),
                ('billingAddressNumber', 'billing_address_number'),
                ('billingAddressComplement', 'billing_address_complement'),
                ('billingAddressDistrict', 'billing_address_district'),
                ('billingAddressPostalCode', 'billing_address_postal_code'),
                ('billingAddressCity', 'billing_address_city'),
                ('billingAddressState', 'billing_address_state'),
            ]

            for key_to_set, key_to_get in credit_card_keys_map:
                params[key_to_set] = self.credit_card.get(key_to_get)

        if self.pre_approval:

            params['preApprovalCharge'] = self.pre_approval.get('charge')
            params['preApprovalName'] = self.pre_approval.get('name')
            params['preApprovalDetails'] = self.pre_approval.get('details')
            params['preApprovalAmountPerPayment'] = self.pre_approval.get(
                'amount_per_payment')
            params['preApprovalMaxAmountPerPayment'] = self.pre_approval.get(
                'max_amount_per_payment')
            params['preApprovalPeriod'] = self.pre_approval.get('period')
            params['preApprovalMaxPaymentsPerPeriod'] = self.pre_approval.get(
                'max_payments_per_period')
            params['preApprovalMaxAmountPerPeriod'] = self.pre_approval.get(
                'max_amount_per_period')
            params['preApprovalInitialDate'] = self.pre_approval.get(
                'initial_date')
            params['preApprovalFinalDate'] = self.pre_approval.get(
                'final_date')
            params['preApprovalMaxTotalAmount'] = self.pre_approval.get(
                'max_total_amount')

        self.data.update(params)
        self.clean_none_params()

    def build_pre_approval_payment_params(self, **kwargs):
        """ build a dict with params """

        params = kwargs or {}

        params['reference'] = self.reference
        params['preApprovalCode'] = self.code

        for i, item in enumerate(self.items, 1):
            params['itemId%s' % i] = item.get('id')
            params['itemDescription%s' % i] = item.get('description')
            params['itemAmount%s' % i] = item.get('amount')
            params['itemQuantity%s' % i] = item.get('quantity')
            params['itemWeight%s' % i] = item.get('weight')
            params['itemShippingCost%s' % i] = item.get('shipping_cost')

        self.data.update(params)
        self.clean_none_params()

    def clean_none_params(self):
        copy = dict(self.data)
        for k, v in list(copy.items()):
            if not v:
                del self.data[k]

    @property
    def reference_prefix(self):
        return self.config.REFERENCE_PREFIX or "%s"

    @reference_prefix.setter
    def reference_prefix(self, value):
        self.config.REFERENCE_PREFIX = (value or "") + "%s"

    @property
    def reference(self):
        return self.reference_prefix % self._reference

    @reference.setter
    def reference(self, value):
        if not isinstance(value, str):
            value = str(value)
        if value.startswith(self.reference_prefix):
            value = value[len(self.reference_prefix):]
        self._reference = value

    def get(self, url):
        """ do a get transaction """
        return requests.get(url, params=self.data, headers=self.config.HEADERS)

    def post(self, url):
        """ do a post request """
        return requests.post(url, data=self.data, headers=self.config.HEADERS)

    def checkout(self, transparent=False, **kwargs):
        """ create a pagseguro checkout """
        self.data['currency'] = self.config.CURRENCY
        self.build_checkout_params(**kwargs)
        if transparent:
            response = self.post(url=self.config.TRANSPARENT_CHECKOUT_URL)
        else:
            response = self.post(url=self.config.CHECKOUT_URL)
        return PagSeguroCheckoutResponse(response.content, config=self.config)

    def transparent_checkout_session(self, **kwargs):
        response = self.post(url=self.config.SESSION_CHECKOUT_URL)
        return PagSeguroCheckoutSession(response.content,
                                        config=self.config).session_id

    def check_notification(self, code):
        """ check a notification by its code """
        response = self.get(url=self.config.NOTIFICATION_URL % code)
        return PagSeguroNotificationResponse(response.content, self.config)

    def check_pre_approval_notification(self, code):
        """ check a notification by its code """
        response = self.get(
            url=self.config.PRE_APPROVAL_NOTIFICATION_URL % code)
        return PagSeguroPreApprovalNotificationResponse(
            response.content, self.config)

    def pre_approval_ask_payment(self, **kwargs):
        """ ask form a subscribe payment """
        self.build_pre_approval_payment_params(**kwargs)
        response = self.post(url=self.config.PRE_APPROVAL_PAYMENT_URL)
        return PagSeguroPreApprovalPayment(response.content, self.config)

    def pre_approval_cancel(self, code):
        """ cancel a subscribe """
        response = self.get(url=self.config.PRE_APPROVAL_CANCEL_URL % code)
        return PagSeguroPreApprovalCancel(response.content, self.config)

    def check_transaction(self, code):
        """ check a transaction by its code """
        response = self.get(url=self.config.TRANSACTION_URL % code)
        return PagSeguroNotificationResponse(response.content, self.config)

    def query_transactions(self, initial_date, final_date,
                           page=None,
                           max_results=None):
        """ query transaction by date range """
        last_page = False
        results = []
        while last_page is False:
            search_result = self._consume_query_transactions(
                initial_date, final_date, page, max_results)
            results.extend(search_result.transactions)
            if search_result.current_page is None or \
               search_result.total_pages is None or \
               search_result.current_page == search_result.total_pages:
                last_page = True
            else:
                page = search_result.current_page + 1

        return results

    def _consume_query_transactions(self, initial_date, final_date,
                                    page=None,
                                    max_results=None):
        querystring = {
            'initialDate': initial_date.strftime('%Y-%m-%dT%H:%M'),
            'finalDate': final_date.strftime('%Y-%m-%dT%H:%M'),
            'page': page,
            'maxPageResults': max_results,
        }
        self.data.update(querystring)
        self.clean_none_params()
        response = self.get(url=self.config.QUERY_TRANSACTION_URL)
        return PagSeguroTransactionSearchResult(response.content, self.config)

    def query_pre_approvals(self, initial_date, final_date, page=None,
                            max_results=None):
        """ query pre-approvals by date range """
        last_page = False
        results = []
        while last_page is False:
            search_result = self._consume_query_pre_approvals(
                initial_date, final_date, page, max_results)
            results.extend(search_result.pre_approvals)
            if search_result.current_page is None or \
               search_result.total_pages is None or \
               search_result.current_page == search_result.total_pages:
                last_page = True
            else:
                page = search_result.current_page + 1

        return results

    def _consume_query_pre_approvals(self, initial_date, final_date, page=None,
                                     max_results=None):
        querystring = {
            'initialDate': initial_date.strftime('%Y-%m-%dT%H:%M'),
            'finalDate': final_date.strftime('%Y-%m-%dT%H:%M'),
            'page': page,
            'maxPageResults': max_results,
        }

        self.data.update(querystring)
        self.clean_none_params()

        response = self.get(url=self.config.QUERY_PRE_APPROVAL_URL)
        return PagSeguroPreApprovalSearch(response.content, self.config)

    def query_pre_approvals_by_code(self, code):
        """ query pre-approvals by code """
        result = self._consume_query_pre_approvals_by_code(code)
        return result

    def _consume_query_pre_approvals_by_code(self, code):

        response = self.get(
            url='%s/%s' % (self.config.QUERY_PRE_APPROVAL_URL, code)
        )
        return PagSeguroPreApproval(response.content, self.config)

    def add_item(self, **kwargs):
        self.items.append(kwargs)
