"""
    **Constants Representing World Wide Currency Symbols and Names**

    this module describes a list of Currency Symbols and Their Names
"""
__developer__ = "mobius-crypt"
__email__ = "mobiusndou@gmail.com"
__twitter__ = "@blueitserver"
__github_profile__ = "https://github.com/freelancing-solutions/"

import typing
from src.config import config_instance
from src.cache import app_cache
from src.utils.utils import return_ttl
from src.singleton import Singleton


class CurrencyUtils(Singleton):
    """
        Utilities to manage Currencies and convert between them
    """
    from src.models.mixins import AmountMixin

    def __init__(self):
        self.currency_list: typing.List[typing.List[str]] = [
            ["ALL", 'Albania Lek'], ["AFN", "Afghanistan Afghani"], ["ARS", "Argentina Peso"],
            ["AWG", "Aruba Guilder"], ["AUD", "Australia Dollar"], ["AZN", "Azerbaijan New Manat"],
            ["BSD", "Bahamas Dollar"], ["BBD", "Barbados Dollar"], ["BYR", "Belarus Ruble"],
            ["BZD", "Belize Dollar"], ["BMD", "Bermuda Dollar"], ["BOB", "Bolivia Boliviano"],
            ["BAM", "Bosnia and Herzegovina Convertible Marka"], ["BWP", "Botswana Pula"],
            ["BGN", "Bulgaria Lev"], ["BRL", "Brazil Real"], ["BND", "Brunei Darussalam Dollar"],
            ["KHR", "Cambodia Riel"], ["CAD", "Canada Dollar"], ["KYD", "Cayman Islands Dollar"],
            ["CLP", "Chile Peso"], ["CNY", "China Yuan Renminbi"], ["COP", "Colombia Peso"],
            ["CRC", "Costa Rica Colon"], ["HRK", "Croatia Kuna"], ["CUP", "Cuba Peso"],
            ["CZK", "Czech Republic Krona"], ["DKK", "Denmark Krone"], ["DOP", "Dominican Republic Peso"],
            ["XCD", "East Caribbean Dollar"], ["EGP", "Egypt Pound"], ["SVC", "El Salvador Colon"],
            ["EEK", "Estonia Kroon"], ["EUR", "Euro Member Countries"], ["FKP", "Falkland Islands (Malvinas) Pound"],
            ["FJD", "Fiji Dollar"], ["GHC", "Ghana Cedis"], ["GIP", "Gibraltar Pound"], ["GTQ", "Guatemala Quetzal"],
            ["GGP", "Guernsey Pound"], ["GYD", "Guyana Dollar"], ["HNL", "Honduras Lempira"],
            ["HKD", "Hong Kong Dollar"],
            ["HUF", "Hungary Forint"], ["ISK", "Iceland Krona"], ["INR", "India Rupee"], ["IDR", "Indonesia Rupiah"],
            ["IRR", "Iran Rial"], ["IMP", "Isle of Man Pound"], ["ILS", "Israel Shekel"], ["JMD", "Jamaica Dollar"],
            ["JPY", "Japan Yen"], ["JEP", "Jersey Pound"], ["KZT", "Kazakhstan Tenge"], ["KPW", "Korea (North) Won"],
            ["KGS", "Kyrgyzstan Som"], ["LAK", "Laos Kip"], ["LVL", "Latvia Lat"], ["LBP", "Lebanon Pound"],
            ["LRD", "Liberia Dollar"], ["LTL", "Lithuania Litas"], ["MKD", "Macedonia Denar"],
            ["MYR", "Malaysia Ringgit"],
            ["MUR", "Mauritius Rupee"], ["MXN", "Mexico Peso"], ["MNT", "Mongolia Tughrik"],
            ["MZN", "Mozambique Metical"],
            ["NAD", "Namibia Dollar"], ["NPR", "Nepal Rupee"], ["ANG", "Netherlands Antilles Guilder"],
            ["NZD", "New Zealand Dollar"], ["NIO", "Nicaragua Cordoba"], ["NGN", "Nigeria Naira"],
            ["NOK", "Norway Krone"],
            ["OMR", "Oman Rial"], ["PKR", "Pakistan Rupee"], ["PAB", "Panama Balboa"], ["PYG", "Paraguay Guarani"],
            ["PEN", "Peru Nuevo Sol"], ["PHP", "Philippines Peso"], ["PLN", "Poland Zloty"], ["QAR", "Qatar Riyal"],
            ["RON", "Romania New Leu"], ["RUB", "Russia Ruble"], ["SHP", "Saint Helena Pound"],
            ["SAR", "Saudi Arabia Riyal"],
            ["RSD", "Serbia Dinar"], ["SCR", "Seychelles Rupee"], ["SGD", "Singapore Dollar"],
            ["SBD", "Solomon Islands Dollar"],
            ["SOS", "Somalia Shilling"], ["ZAR", "South Africa Rand"], ["KRW", "Korea (South) Won"],
            ["LKR", "Sri Lanka Rupee"],
            ["SEK", "Sweden Krona"], ["CHF", "Switzerland Franc"], ["SRD", "Suriname Dollar"], ["SYP", "Syria Pound"],
            ["TWD", "Taiwan New Dollar"], ["THB", "Thailand Baht"], ["TTD", "Trinidad and Tobago Dollar"],
            ["TRY", "Turkey Lira"], ["TRL", "Turkey Lira"], ["TVD", "Tuvalu Dollar"], ["UAH", "Ukraine Hryvna"],
            ["GBP", "United Kingdom Pound"], ["USD", "United States Dollar"], ["UYU", "Uruguay Peso"],
            ["UZS", "Uzbekistan Som"],
            ["VEF", "Venezuela Bolivar"], ["VND", "Viet Nam Dong"], ["YER", "Yemen Rial"], ["ZWD", "Zimbabwe Dollar"],
            ["GBX", "United Kingdom Penny Sterling"]]

    def currency_symbols(self) -> typing.List[str]:
        """
            returns currency symbols only
        :return:
        """
        return [currency[0] for currency in self.currency_list]

    def get_currencies(self) -> typing.List[tuple]:
        """
            **get_currencies**
                returns a tuple with currency symbols and definitions
            :return: List of Tuples
        """
        return [(currency[0], currency[1]) for currency in self.currency_list]

    @staticmethod
    def get_conversion_rate(from_symbol: str, to_symbol: str) -> typing.Union[float, None]:
        """
        **get_conversion_rate**

            :param from_symbol:
            :param to_symbol:
            :return: float number representing the conversion rate
        """
        # TODO- use an api to get the present conversion_rate
        pass

    @app_cache.cache.memoize(timeout=return_ttl('short'))
    def currency_conversion(self, from_amount: AmountMixin, convert_to_symbol: str) -> typing.Union[AmountMixin, None]:
        """
            given an origin amount convert to any supported currency
        :param from_amount:
        :param convert_to_symbol:
        :return:
        """
        conversion_rate: typing.Union[float, None] = self.get_conversion_rate(from_symbol=from_amount.currency,
                                                                              to_symbol=convert_to_symbol)
        if convert_to_symbol is not None:
            from_amount.currency = convert_to_symbol
            converted = from_amount.amount_cents * conversion_rate
            from_amount.amount_cents = int(converted)
            return from_amount
        return None


currency_util: CurrencyUtils = CurrencyUtils()
del CurrencyUtils


if __name__ == '__main__':
    """
        quick tests here
    """
    pass
