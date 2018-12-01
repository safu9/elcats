import calendar
import datetime


class BaseCalendarMixin:
    """ カレンダー関連Mixinの基底クラス """
    first_weekday = calendar.MONDAY  # 最初に表示される曜日

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


class MonthCalendarMixin(BaseCalendarMixin):
    """ 月間カレンダーの機能を提供するMixin """

    @staticmethod
    def get_previous_month(date):
        """ 前月を返す """
        if date.month == 1:
            return date.replace(year=date.year-1, month=12, day=1)
        else:
            return date.replace(month=date.month-1, day=1)

    @staticmethod
    def get_next_month(date):
        """ 次月を返す """
        if date.month == 12:
            return date.replace(year=date.year+1, month=1, day=1)
        else:
            return date.replace(month=date.month+1, day=1)

    def get_month_days(self, date):
        """ その月の全ての日を返す """
        return list(self._calendar.itermonthdates(date.year, date.month))

    def get_current_month(self):
        """ 現在の月を返す """
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')

        if month and year:
            return datetime.date(year=int(year), month=int(month), day=1)
        else:
            return datetime.date.today().replace(day=1)

    def get_month_calendar(self):
        """ 月間カレンダー情報の入った辞書を返す """
        self.setup()
        current_month = self.get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            'days': self.get_month_days(current_month),
            'current': current_month,
            'previous': self.get_previous_month(current_month),
            'next': self.get_next_month(current_month),
        }
        return calendar_data
