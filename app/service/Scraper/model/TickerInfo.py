class TickerInfo():
	
    def __init__(self):
        self.ticker = None
        self.price = None
        self.dy = None
        self.pvp = None
        self.segment = None
        self.type_anbima = None
        self.segment_anbima = None
        self.roe = None
        self.dl_ebitda = None
        self.sector = None
        self.sub_sector = None
 
    def convert_to_float(self, value):
        if value.strip() == "-":
            return "-"
        return float(value.replace(".", "").replace(",", ".").replace("%", ""))
    
    def set_ticker(self, ticker):
        self.ticker = ticker

    def set_price(self, price):
        self.price = self.convert_to_float(price)

    def set_dy(self, dy):
        self.dy = self.convert_to_float(dy)

    def set_pvp(self, pvp):
        self.pvp = self.convert_to_float(pvp)

    def set_segment(self, segment):
        self.segment = segment

    def set_type_anbima(self, type_anbima):
        self.type_anbima = type_anbima

    def set_segment_anbima(self, segment_anbima):
        self.segment_anbima = segment_anbima

    def set_roe(self, roe):
        self.roe = self.convert_to_float(roe)

    def set_dl_ebitda(self, dl_ebitda):
        self.dl_ebitda = self.convert_to_float(dl_ebitda)

    def set_sector(self, sector):
        self.sector = sector

    def set_sub_sector(self, sub_sector): 
        self.sub_sector = sub_sector