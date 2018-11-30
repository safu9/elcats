import calendar
import datetime


class BaseCalendarMixin:
    """ カレンダー関連Mixinの基底クラス """
    first_weekday = 0  # 最初に表示される曜日。0:月曜、1:火曜、6:日曜

    def setup(self):
        """ カレンダーのセットアップ処理 """
        self._calendar = calendar.Calendar(self.first_weekday)


class WeekCalendarMixin(BaseCalendarMixin):
    """ 週間カレンダーの機能を提供するMixin """

    def get_week_days(self):
        """ その週の日を全て返す """
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')

        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()

        for week in self._calendar.monthdatescalendar(date.year, date.month):
            if date in week:  # 週ごとのdatetime.date型のリスト
                return week

    def get_week_calendar(self):
        """ 週間カレンダー情報の入った辞書を返す """
        self.setup()
        days = self.get_week_days()
        first = days[0]
        last = days[-1]
        calendar_data = {
            'now': datetime.date.today(),
            'days': days,
            'next': first + datetime.timedelta(days=7),
            'previous': first - datetime.timedelta(days=7),
            'first': first,
            'last': last,
        }
        return calendar_data
