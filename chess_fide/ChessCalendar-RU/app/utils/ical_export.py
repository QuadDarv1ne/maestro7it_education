"""
iCalendar export functionality for tournaments
"""

from datetime import datetime, timedelta
from typing import List
import re


class ICalExporter:
    """Export tournaments to iCalendar format"""
    
    @staticmethod
    def escape_text(text: str) -> str:
        """Escape special characters for iCal format"""
        if not text:
            return ""
        
        # Replace special characters
        text = text.replace('\\', '\\\\')
        text = text.replace(',', '\\,')
        text = text.replace(';', '\\;')
        text = text.replace('\n', '\\n')
        
        return text
    
    @staticmethod
    def format_datetime(dt: datetime) -> str:
        """Format datetime for iCal (YYYYMMDDTHHMMSSZ)"""
        if not dt:
            return ""
        
        # Convert to UTC if needed
        return dt.strftime('%Y%m%dT%H%M%SZ')
    
    @staticmethod
    def format_date(dt: datetime) -> str:
        """Format date for iCal (YYYYMMDD)"""
        if not dt:
            return ""
        
        return dt.strftime('%Y%m%d')
    
    @staticmethod
    def generate_uid(tournament_id: int, domain: str = "chesscalendar.ru") -> str:
        """Generate unique identifier for event"""
        return f"tournament-{tournament_id}@{domain}"
    
    @staticmethod
    def create_event(tournament) -> str:
        """Create iCal event for a single tournament"""
        lines = []
        
        lines.append("BEGIN:VEVENT")
        
        # UID - unique identifier
        uid = ICalExporter.generate_uid(tournament.id)
        lines.append(f"UID:{uid}")
        
        # DTSTAMP - creation timestamp
        dtstamp = ICalExporter.format_datetime(datetime.utcnow())
        lines.append(f"DTSTAMP:{dtstamp}")
        
        # DTSTART - start date
        if tournament.start_date:
            dtstart = ICalExporter.format_date(tournament.start_date)
            lines.append(f"DTSTART;VALUE=DATE:{dtstart}")
        
        # DTEND - end date (add 1 day for all-day events)
        if tournament.end_date:
            # For all-day events, end date is exclusive
            end_date = tournament.end_date + timedelta(days=1)
            dtend = ICalExporter.format_date(end_date)
            lines.append(f"DTEND;VALUE=DATE:{dtend}")
        
        # SUMMARY - event title
        summary = ICalExporter.escape_text(tournament.name)
        lines.append(f"SUMMARY:{summary}")
        
        # DESCRIPTION - event description
        description_parts = []
        
        if tournament.description:
            description_parts.append(tournament.description)
        
        if tournament.category:
            description_parts.append(f"Категория: {tournament.category}")
        
        if tournament.time_control:
            description_parts.append(f"Контроль времени: {tournament.time_control}")
        
        if tournament.prize_fund:
            description_parts.append(f"Призовой фонд: {tournament.prize_fund}")
        
        if tournament.average_rating:
            description_parts.append(f"Рейтинг: {tournament.average_rating:.1f}/5")
        
        # Add link
        description_parts.append(f"\\nПодробнее: https://chesscalendar.ru/tournament/{tournament.id}")
        
        description = ICalExporter.escape_text("\\n".join(description_parts))
        lines.append(f"DESCRIPTION:{description}")
        
        # LOCATION - event location
        if tournament.location:
            location = ICalExporter.escape_text(tournament.location)
            lines.append(f"LOCATION:{location}")
        
        # URL - event URL
        url = f"https://chesscalendar.ru/tournament/{tournament.id}"
        lines.append(f"URL:{url}")
        
        # STATUS
        status_map = {
            'upcoming': 'CONFIRMED',
            'ongoing': 'CONFIRMED',
            'completed': 'CONFIRMED',
            'cancelled': 'CANCELLED'
        }
        status = status_map.get(tournament.status, 'CONFIRMED')
        lines.append(f"STATUS:{status}")
        
        # CATEGORIES
        if tournament.category:
            categories = ICalExporter.escape_text(tournament.category)
            lines.append(f"CATEGORIES:{categories}")
        
        # ORGANIZER
        if tournament.organizer:
            organizer = ICalExporter.escape_text(tournament.organizer)
            lines.append(f"ORGANIZER;CN={organizer}:MAILTO:info@chesscalendar.ru")
        
        # ALARM - reminder 1 day before
        lines.append("BEGIN:VALARM")
        lines.append("TRIGGER:-P1D")
        lines.append("ACTION:DISPLAY")
        lines.append(f"DESCRIPTION:Напоминание: {summary}")
        lines.append("END:VALARM")
        
        lines.append("END:VEVENT")
        
        return "\r\n".join(lines)
    
    @staticmethod
    def export_tournament(tournament) -> str:
        """Export single tournament to iCal format"""
        lines = []
        
        # Calendar header
        lines.append("BEGIN:VCALENDAR")
        lines.append("VERSION:2.0")
        lines.append("PRODID:-//ChessCalendar-RU//Tournament Calendar//RU")
        lines.append("CALSCALE:GREGORIAN")
        lines.append("METHOD:PUBLISH")
        lines.append("X-WR-CALNAME:Шахматный турнир")
        lines.append("X-WR-TIMEZONE:Europe/Moscow")
        lines.append("X-WR-CALDESC:Турнир из ChessCalendar-RU")
        
        # Add event
        lines.append(ICalExporter.create_event(tournament))
        
        # Calendar footer
        lines.append("END:VCALENDAR")
        
        return "\r\n".join(lines)
    
    @staticmethod
    def export_tournaments(tournaments: List, calendar_name: str = "Шахматные турниры") -> str:
        """Export multiple tournaments to iCal format"""
        lines = []
        
        # Calendar header
        lines.append("BEGIN:VCALENDAR")
        lines.append("VERSION:2.0")
        lines.append("PRODID:-//ChessCalendar-RU//Tournament Calendar//RU")
        lines.append("CALSCALE:GREGORIAN")
        lines.append("METHOD:PUBLISH")
        lines.append(f"X-WR-CALNAME:{ICalExporter.escape_text(calendar_name)}")
        lines.append("X-WR-TIMEZONE:Europe/Moscow")
        lines.append("X-WR-CALDESC:Календарь турниров из ChessCalendar-RU")
        
        # Add events
        for tournament in tournaments:
            lines.append(ICalExporter.create_event(tournament))
        
        # Calendar footer
        lines.append("END:VCALENDAR")
        
        return "\r\n".join(lines)
    
    @staticmethod
    def export_user_favorites(user_id: int) -> str:
        """Export user's favorite tournaments"""
        from app.models.favorite import FavoriteTournament
        from app.models.tournament import Tournament
        
        favorites = FavoriteTournament.query.filter_by(user_id=user_id).all()
        tournaments = [f.tournament for f in favorites if f.tournament]
        
        return ICalExporter.export_tournaments(
            tournaments,
            calendar_name="Мои избранные турниры"
        )
    
    @staticmethod
    def export_upcoming_tournaments(days: int = 30) -> str:
        """Export upcoming tournaments for next N days"""
        from app.models.tournament import Tournament
        from datetime import datetime, timedelta
        
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=days)
        
        tournaments = Tournament.query.filter(
            Tournament.start_date >= start_date,
            Tournament.start_date <= end_date
        ).order_by(Tournament.start_date).all()
        
        return ICalExporter.export_tournaments(
            tournaments,
            calendar_name=f"Турниры на {days} дней"
        )


def create_ical_response(ical_content: str, filename: str = "tournament.ics"):
    """Create Flask response with iCal content"""
    from flask import Response
    
    response = Response(ical_content, mimetype='text/calendar')
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
    
    return response
