from app import db
from app.models.user import User
from app.models.forum import ForumThread, ForumPost
from app.models.report import Report
from datetime import datetime


class ReportingService:
    """Service for handling content reports"""
    
    @staticmethod
    def submit_report(reporter_id, reported_type, reported_id, reason, description=None):
        """Submit a report for inappropriate content"""
        # Validate inputs
        reporter = User.query.get(reporter_id)
        if not reporter or not reporter.is_regular_user:
            raise ValueError("Invalid reporter")
        
        if reported_type not in ['thread', 'post']:
            raise ValueError("Reported type must be 'thread' or 'post'")
        
        # Validate that the reported content exists
        if reported_type == 'thread':
            content = ForumThread.query.get(reported_id)
        else:  # 'post'
            content = ForumPost.query.get(reported_id)
        
        if not content:
            raise ValueError(f"{reported_type.capitalize()} not found")
        
        if not reason or len(reason.strip()) == 0:
            raise ValueError("Reason cannot be empty")
        
        # Check if a similar unresolved report already exists
        existing_report = Report.query.filter_by(
            reporter_id=reporter_id,
            reported_type=reported_type,
            reported_id=reported_id,
            is_resolved=False
        ).first()
        
        if existing_report:
            raise ValueError("A report for this content already exists and is pending resolution")
        
        # Create the report
        report = Report(
            reporter_id=reporter_id,
            reported_type=reported_type,
            reported_id=reported_id,
            reason=reason,
            description=description
        )
        
        db.session.add(report)
        db.session.commit()
        
        return report
    
    @staticmethod
    def resolve_report(report_id, resolver_id, resolution_notes=None):
        """Mark a report as resolved"""
        report = Report.query.get(report_id)
        if not report:
            raise ValueError("Report not found")
        
        if report.is_resolved:
            raise ValueError("Report is already resolved")
        
        # Verify resolver is an admin
        resolver = User.query.get(resolver_id)
        if not resolver or not resolver.is_admin:
            raise ValueError("Only admins can resolve reports")
        
        report.is_resolved = True
        report.resolved_at = datetime.utcnow()
        report.resolved_by = resolver_id
        report.resolution_notes = resolution_notes
        
        db.session.commit()
        return report
    
    @staticmethod
    def get_report(report_id):
        """Get a specific report by ID"""
        report = Report.query.get(report_id)
        if report:
            return report.to_dict()
        return None
    
    @staticmethod
    def get_reports_for_content(reported_type, reported_id):
        """Get all reports for a specific piece of content"""
        reports = Report.query.filter_by(
            reported_type=reported_type,
            reported_id=reported_id
        ).all()
        
        return [report.to_dict() for report in reports]
    
    @staticmethod
    def get_unresolved_reports(page=1, per_page=10):
        """Get all unresolved reports with pagination"""
        query = Report.query.filter_by(is_resolved=False).order_by(Report.created_at.desc())
        reports = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'reports': [report.to_dict() for report in reports.items],
            'pagination': {
                'page': reports.page,
                'pages': reports.pages,
                'per_page': reports.per_page,
                'total': reports.total
            }
        }
    
    @staticmethod
    def get_user_reports(user_id, page=1, per_page=10):
        """Get reports submitted by a specific user"""
        query = Report.query.filter_by(reporter_id=user_id).order_by(Report.created_at.desc())
        reports = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'reports': [report.to_dict() for report in reports.items],
            'pagination': {
                'page': reports.page,
                'pages': reports.pages,
                'per_page': reports.per_page,
                'total': reports.total
            }
        }
    
    @staticmethod
    def get_all_reports(page=1, per_page=10):
        """Get all reports (admin function)"""
        # Verify this is called by an admin
        # In a real application, you'd pass the user_id and check permissions
        
        query = Report.query.order_by(Report.created_at.desc())
        reports = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'reports': [report.to_dict() for report in reports.items],
            'pagination': {
                'page': reports.page,
                'pages': reports.pages,
                'per_page': reports.per_page,
                'total': reports.total
            }
        }
    
    @staticmethod
    def delete_report(report_id, deleter_id):
        """Delete a report (admin function)"""
        report = Report.query.get(report_id)
        if not report:
            raise ValueError("Report not found")
        
        deleter = User.query.get(deleter_id)
        if not deleter or not deleter.is_admin:
            raise ValueError("Only admins can delete reports")
        
        db.session.delete(report)
        db.session.commit()
        return True