from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' 
app.config['SECRET_KEY'] = 'mai_flask'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    employees_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Company {self.name}>"





@app.route('/companies')
def list_companies():
    companies = Company.query.all()
    return render_template('companies.html', companies=companies)
  
@app.route('/create_company', methods=['POST'])
def create_company():
    name = request.form.get('name')
    location = request.form.get('location')
    description = request.form.get('description')
    employees_count = request.form.get('employees_count')
    
    new_company = Company(name=name, location=location, description=description, employees_count=employees_count)
    db.session.add(new_company)
    db.session.commit()

    return "Company created successfully!"

@app.route('/update/company/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    company = Company.query.get(company_id)

    if company:

        name = request.form.get('name')
        location = request.form.get('location')
        description = request.form.get('description')
        employees_count = request.form.get('employees_count')

        company.name = name
        company.location = location
        company.description = description
        company.employees_count = employees_count

        db.session.commit()
        return "Company updated successfully!"


class CompanyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    employees_count = StringField('Employees Count', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/create_company', methods=['GET', 'POST']) 

def create_company_form():
    form = CompanyForm()
    if form.validate_on_submit():
        name = form.name.data
        location = form.location.data
        description = form.description.data
        employees_count = form.employees_count.data
        
        new_company = Company(name=name, location=location, description=description, employees_count=employees_count)
        db.session.add(new_company)
        db.session.commit()

        return "Company created successfully!"

    return render_template('create_company.html', form=form)

# if __name__ == '__main__':
#     app.run(debug=True)


