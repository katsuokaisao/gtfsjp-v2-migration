from model.agency_jp import AgencyJP
from model.agency import Agency
from model.calendar_date import CalendarDate
from model.calendar import Calendar
from model.fare_attribute import FareAttribute
from model.fare_rule import FareRule
from model.feed_info import FeedInfo
from model.frequency import Frequency
from model.office_jp import OfficeJP
from model.route import Route
from model.route_jp import RouteJP
from model.shape import Shape
from model.stop_time import StopTime
from model.stop import Stop
from model.transfer import Transfer
from model.translation import Translation
from model.trip import Trip


target_classes = [
    AgencyJP,
    Agency,
    CalendarDate,
    Calendar,
    FareAttribute,
    FareRule,
    FeedInfo,
    Frequency,
    OfficeJP,
    Route,
    RouteJP,
    Shape,
    StopTime,
    Stop,
    Transfer,
    Translation,
    Trip,
]
