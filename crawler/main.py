from typing import List
from scrapy import Spider, Selector, Request
from scrapy.http import Response

class NvidiaCrawler(Spider):
    name = "nvidia-compute-capability"
    
    _new_GPUS_url = "https://developer.nvidia.com/cuda/gpus"
    _legacy_GPUS_url = "https://developer.nvidia.com/cuda/gpus/legacy"
    _urls = [_new_GPUS_url, _legacy_GPUS_url]

    _table_xpath = '//*[@id="isy0j"]'
    _num_of_columns = 4

    out_data = {}

    async def start(self):
        for url in self._urls:
            yield Request(
                url,
                callback=self._next_request,
                dont_filter=True,
            )

    def _next_request(self, response:Response) -> Request:
        self.parse(response)

        if(response.url == self._urls[-1]):
            yield self.out_data


    def parse(self, response:Response):
        if(response.status != 200):
            return None
            
        
        table = response.xpath(self._table_xpath).get()
        if(table is None):
            return None

        trs = Selector(text=table).css("tr").getall()
        for tr in trs:
            tds = Selector(text=tr).css('td').getall()
            if(len(tds) != self._num_of_columns): 
                continue

            compute_capability = self._parse_compute_capability(tds[0])
            data_centers = self._parse_data_centers(tds[1])
            workstations = self._parse_workstations(tds[2])
            jetson = self._parse_jetson(tds[3])

            self.out_data[compute_capability] = {
                    "data_centers_boards":data_centers,
                    "workstations":workstations,
                    "jetson_boards":jetson
            }

    def _parse_compute_capability(self, td:str) -> str:
        compute_capability = Selector(text=td).xpath('//div/text()').get()
        return 'failed' if compute_capability is None else compute_capability

    def _parse_data_centers(self, td:str) -> List[str]:
        data = self._parse_multiple_from_td(td)
        return data
    
    def _parse_workstations(self, td:str) -> List[str]:
        data = self._parse_multiple_from_td(td)
        return data
    
    def _parse_jetson(self, td:str) -> List[str]:
        data = self._parse_multiple_from_td(td)
        return data
        
    def _parse_multiple_from_td(self, td:str) -> List[str]:
        data = Selector(text=td).xpath('//div').get()
        if(data is None):
            return []

        data = data.replace('<br>', '@')
        return [ elem.strip().replace('*','') for elem in Selector(text=data).xpath('//div/text()').get().split('@')]



