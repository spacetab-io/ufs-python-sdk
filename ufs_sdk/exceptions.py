from .wrapper import AdditionalInfoTrainList


class UfsAPIError(Exception):
    __slots__ = ['code', 'message']

    def __init__(self, method, error_data):
        super(UfsAPIError, self).__init__()
        self.method = method
        self.error_data = error_data

    def __str__(self):
        msg = 'Method: %s\n' % self.method
        for item in self.error_data:
            msg += '    %s: %s\n' % (item.tag, item.text)
        return msg


class UfsTrainListError(Exception):
    __slots__ = ['code', 'message', 'additional_info']

    def __init__(self, method, error_data):
        super(UfsTrainListError, self).__init__()
        self.method = method
        self.error_data = error_data
        self.additional_info = AdditionalInfoTrainList(error_data.find('./AdditionalInfo'))

    def __str__(self):
        msg = 'Method: %s\n' % self.method
        for item in self.error_data:
            msg += '    %s: %s\n' % (item.tag, item.text)

        is_allowed = self.additional_info.xml.find('./IsAllowedMultiStationSearch')
        msg += '      %s: %s\n' % (is_allowed.tag, is_allowed.text)
        for item in self.additional_info.xml.find('./Stations'):
            msg += '      %s:' % item.tag
            for station in item:
                msg += '        %s: %s\n' % (station.tag, station.text)

        return msg

