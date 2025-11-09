"""Database models for the Color Detector application."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ColorHistory(db.Model):
    """Model for storing color detection history."""
    
    __tablename__ = 'color_history'
    
    id = db.Column(db.Integer, primary_key=True)
    hex_code = db.Column(db.String(7), nullable=False)
    color_name = db.Column(db.String(100), nullable=False)
    rgb_r = db.Column(db.Integer, nullable=False)
    rgb_g = db.Column(db.Integer, nullable=False)
    rgb_b = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.String(100), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'hex_code': self.hex_code,
            'color_name': self.color_name,
            'rgb': {
                'r': self.rgb_r,
                'g': self.rgb_g,
                'b': self.rgb_b
            },
            'created_at': self.created_at.isoformat()
        }


class ColorPalette(db.Model):
    """Model for storing saved color palettes."""
    
    __tablename__ = 'color_palettes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    colors = db.Column(db.JSON, nullable=False)  # List of hex codes
    session_id = db.Column(db.String(100), index=True)
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'colors': self.colors,
            'is_favorite': self.is_favorite,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class BrandCollection(db.Model):
    """Model for brand color collections."""
    
    __tablename__ = 'brand_collections'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(500))
    primary_colors = db.Column(db.JSON, nullable=False)  # List of hex codes
    secondary_colors = db.Column(db.JSON)  # Optional secondary colors
    project_type = db.Column(db.String(100))  # e.g., "client", "personal"
    client_name = db.Column(db.String(200))
    session_id = db.Column(db.String(100), index=True)
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'logo_url': self.logo_url,
            'primary_colors': self.primary_colors,
            'secondary_colors': self.secondary_colors,
            'project_type': self.project_type,
            'client_name': self.client_name,
            'is_archived': self.is_archived,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class FavoriteColor(db.Model):
    """Model for user's favorite colors."""
    
    __tablename__ = 'favorite_colors'
    
    id = db.Column(db.Integer, primary_key=True)
    hex_code = db.Column(db.String(7), nullable=False)
    color_name = db.Column(db.String(100))
    notes = db.Column(db.Text)
    tags = db.Column(db.JSON)  # List of tags
    session_id = db.Column(db.String(100), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'hex_code': self.hex_code,
            'color_name': self.color_name,
            'notes': self.notes,
            'tags': self.tags or [],
            'created_at': self.created_at.isoformat()
        }


class ColorAnalytics(db.Model):
    """Model for tracking color usage analytics."""
    
    __tablename__ = 'color_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    hex_code = db.Column(db.String(7), nullable=False, index=True)
    action_type = db.Column(db.String(50), nullable=False)  # detect, save, export, etc.
    session_id = db.Column(db.String(100), index=True)
    analytics_data = db.Column(db.JSON)  # Additional tracking data
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'hex_code': self.hex_code,
            'action_type': self.action_type,
            'metadata': self.analytics_data,
            'created_at': self.created_at.isoformat()
        }


class SharedPalette(db.Model):
    """Model for shared/collaborative palettes."""
    
    __tablename__ = 'shared_palettes'
    
    id = db.Column(db.Integer, primary_key=True)
    palette_id = db.Column(db.Integer, db.ForeignKey('color_palettes.id'), nullable=False)
    share_token = db.Column(db.String(100), unique=True, nullable=False, index=True)
    owner_session_id = db.Column(db.String(100), nullable=False)
    can_edit = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    palette = db.relationship('ColorPalette', backref='shares')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'palette_id': self.palette_id,
            'share_token': self.share_token,
            'can_edit': self.can_edit,
            'view_count': self.view_count,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat()
        }


class PaletteComment(db.Model):
    """Model for comments on shared palettes."""
    
    __tablename__ = 'palette_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    palette_id = db.Column(db.Integer, db.ForeignKey('color_palettes.id'), nullable=False)
    author_name = db.Column(db.String(100))
    comment_text = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    palette = db.relationship('ColorPalette', backref='comments')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'palette_id': self.palette_id,
            'author_name': self.author_name or 'Anonymous',
            'comment_text': self.comment_text,
            'created_at': self.created_at.isoformat()
        }


class Gradient(db.Model):
    """Model for saved gradients."""
    
    __tablename__ = 'gradients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    colors = db.Column(db.JSON, nullable=False)  # List of hex codes
    gradient_type = db.Column(db.String(50))  # linear, radial, conic
    css_code = db.Column(db.Text)
    session_id = db.Column(db.String(100), index=True)
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'colors': self.colors,
            'gradient_type': self.gradient_type,
            'css_code': self.css_code,
            'is_favorite': self.is_favorite,
            'created_at': self.created_at.isoformat()
        }
