import re
import json
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter

class Convertor:
    check_conversion_pattern = r"\d+\s*\w+\s+(in|to)\s+\w+"
    split_conversion_pattern = r"(\d+)|(\w+)"
    conversions = json.load(open('conversions.json', 'r'))
    aliases = json.load(open('aliases.json', 'r'))

    def parse_arg(self, arg):
        pattern = self.split_conversion_pattern
        arg_list = re.findall(pattern, arg)
        arg_list = ["".join(x) for x in arg_list]
        val, src_unit, _, target_unit = arg_list
        src_unit, target_unit = src_unit.lower(), target_unit.lower()
        val = float(val)
        return val, src_unit, target_unit

    def convert(self, value, source, target, conv):
        source, target = map(self.translate_unit, (source, target))
        if source in conv and target in conv[source]:
            return value * conv[source][target]

        elif target in conv and source in conv[target]:
            return value / conv[target][source]

        elif self.run_complex_conversion(value, source, target, conv) is not None:
            return self.run_complex_conversion(value, source, target, conv)

        else:
            raise Exception('Error: unit not found')

    def convert_unit(self, value, source, target):
        return self.convert(value, source, target, self.conversions)

    def convert_currency(self, value, source, target):
        source, target = source.upper(), target.upper()
        
        if source.upper() == "BTC": 
            return BtcConverter().convert_btc_to_cur(value, target)
        
        elif target.upper() == "BTC":
            return BtcConverter().convert_to_btc(value, source)

        self.currency_converter = CurrencyRates()
        return self.currency_converter.convert(source, target, value)

    def run_complex_conversion(self, value, source, target, conv):
        for temp_unit in conv:
            if source in conv[temp_unit] and target in conv[temp_unit]:
                temp_conversion = self.convert(value, source, temp_unit, conv)
                return self.convert(temp_conversion, temp_unit, target, conv)
        return None

    def translate_unit(self, unit):
        for k in self.aliases.keys():
            if unit == k:
                return unit
            else:
                for val in self.aliases[k]:
                    if unit == val:
                        return k
        return unit

    def is_conversion_like(self, arg):
        pattern = self.check_conversion_pattern
        return re.fullmatch(pattern, arg)
