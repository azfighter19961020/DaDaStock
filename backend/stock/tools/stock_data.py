
import pytz
import datetime
from enum import Enum

class TimeZone(Enum):
	AsiaTimeZone = pytz.timezone("Asia/Shanghai")
	GMTTimeZone = pytz.timezone("Etc/GMT+8")
	UTCTimeZone = pytz.timezone("UTC")

class TimeZoneFactory:
	def __init__(self):
		self.timezoneEnum = TimeZone

	def getTimeZone(self,timezone):
		if timezone == "Asia":
			return self.timezoneEnum.AsiaTimeZone.value
		elif timezone == "GMT":
			return self.timezoneEnum.GMTTimeZone.value
		elif timezone == "UTC":
			return self.timezoneEnum.UTCTimeZone.value
		else:
			raise Exception("Timezone not in list!")


class stockDataHelper:
	def __init__(self):
		self.fac = TimeZoneFactory()
		self.startTerminateDate = None
		self.endTerminateDate = None
		self.startTerminateTuple = (13,30)
		self.endTerminateTuple = (17,59)

	def __nowDate(self):
		return self.timezoneTransformer(datetime.datetime.now(),"UTC")

	def __initializeTerminateDate(self):
		date = self.__nowDate()
		self.startTerminateDate = self.timezoneTransformer(datetime.datetime(
												date.year,
												date.month,
												date.day,
												*self.startTerminateTuple,
												tzinfo=self.fac.getTimeZone("GMT")
												),"UTC")
		self.endTerminateDate = self.timezoneTransformer(datetime.datetime(
												date.year,
												date.month,
												date.day,
												*self.endTerminateTuple,
												tzinfo=self.fac.getTimeZone("GMT")
												),"UTC")

	def compare(self,nowdate):
		return self.startTerminateDate < nowdate < self.endTerminateDate

	def now(self):
		self.__initializeTerminateDate()
		nowdate = self.__nowDate()
		if self.compare(nowdate):
			print("self.startTerminateDate < nowdate < endTerminateDate")
			nowdate = nowdate - datetime.timedelta(days = 1)
		elif nowdate.hour >= self.endTerminateDate.hour + 1:
			print("nowdate.hour >= self.endTerminateDate.hour + 1")
			nowdate = nowdate - datetime.timedelta(hours = 9)
		print("now date:",nowdate)
		return nowdate

	def getNowByAsia(self):
		sdate = self.timezoneTransformer(self.now(),"Asia")
		return datetime.datetime(
				sdate.year,
				sdate.month,
				sdate.day,
				sdate.hour,
				sdate.minute,
				tzinfo = self.fac.getTimeZone("UTC")
			)

	def stockDateCheck(self,stockDate):
		sdate = self.timezoneTransformer(datetime.datetime(
											stockDate.year,
											stockDate.month,
											stockDate.day,
											stockDate.hour,
											stockDate.minute,
											tzinfo = self.fac.getTimeZone("Asia")
										),"UTC")
		return self.__timestampHelper(sdate) <= self.__timestampHelper(self.now()) - (60 * 6)

	def specifyDateCheck(self,stockDate,sd,ed,isToday):
		# sd = sd.astimezone(self.timezone.UTCTimezone)
		# ed = ed.astimezone(self.timezone.UTCTimezone)
		sd = self.timezoneTransformer(sd,"UTC")
		ed = self.timezoneTransformer(ed,"UTC")
		if not isToday:
			ed = ed + datetime.timedelta(days = 1)
		sdate = self.timezoneTransformer(datetime.datetime(
							stockDate.year,
							stockDate.month,
							stockDate.day,
							stockDate.hour,
							stockDate.minute,
							tzinfo = self.fac.getTimeZone("Asia")
						),"UTC")
		return self.__timestampHelper(sd) <= self.__timestampHelper(sdate) <= self.__timestampHelper(ed) - (60 * 6)

	def __timestampHelper(self,time):
		return datetime.datetime.timestamp(time)

	def timezoneTransformer(self,time,type):
		return time.astimezone(self.fac.getTimeZone(type))

	def specifyToAsia(self):
		return self.timezoneTransformer(self.now(),"Asia")

	def isTrade(self):
		nowDate = self.timezoneTransformer(self.__nowDate(),"Asia")
		return (nowDate.hour >= 13) and (nowDate.hour < 18)


# s = stockDataHelper()
# s.now()
# print(s.startTerminateDate)

s = stockDataHelper()
print(s.specifyToAsia())




