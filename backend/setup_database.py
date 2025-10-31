import os
import sys
from datetime import datetime

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def setup_database():
    try:
        from app import create_app, db
        
        # Create app
        app = create_app()
        
        with app.app_context():
            # Drop all existing tables and create new ones
            db.drop_all()
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create admin user
            from app.models.user import User
            from app.models.category import Category
            
            admin = User.query.filter_by(email='admin@blog.com').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@blog.com',
                    role='admin',
                    bio='System Administrator'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                print("✅ Admin user created")
            
            # Create sample categories
            categories = [
                ('Technology', 'Latest tech trends and innovations', '#3b82f6'),
                ('Business', 'Business strategies and market insights', '#10b981'),
                ('Innovation', 'Creative ideas and breakthrough technologies', '#8b5cf6'),
                ('Development', 'Software development best practices', '#f59e0b'),
                ('AI & ML', 'Artificial Intelligence and Machine Learning', '#ef4444')
            ]
            
            for name, description, color in categories:
                if not Category.query.filter_by(name=name).first():
                    category = Category(
                        name=name,
                        description=description,
                        color=color
                    )
                    db.session.add(category)
                    print(f"✅ Category '{name}' created")
            
            db.session.commit()
            print("🎉 Database setup complete!")
            print("📧 Admin: admin@blog.com")
            print("🔑 Password: admin123")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    setup_database()
