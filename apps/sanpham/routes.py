from flask import redirect, render_template, url_for, flash, request,session
from apps import db, app, photos
from .models import Category, addsp
from .forms import Addsp
import secrets
from datetime import datetime


@app.route('/addCate', methods=['GET', 'POST'])
def addCate(): #Thêm loại
    if 'username' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        getcate = request.form.get('cate')
        cate = Category(name=getcate)
        db.session.add(cate)
        flash(f'Loại {getcate} đã được thêm vào database', 'success')
        db.session.commit()
        return redirect(url_for('addCate'))
    return render_template('sanpham/addCate.html')

 #bắt đầu minh #
@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'username' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('sanpham/updatecat.html', title='cập nhập loại',updatecat=updatecat)

    #kết thúc#

@app.route('/addSp', methods=['GET', 'POST'])
def addSp():
    if 'username' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    form = Addsp(request.form)
    categories = Category.query.all()
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        decs = form.discription.data
        image = photos.save(request.files.get('image'), name=secrets.token_hex(10)+ ".")
        date = datetime.now()
        category = request.form.get('category')
        
        addSanpham = addsp(name=name,price=price,decs = decs, pub_date=date, 
        category_id= category ,image=image)
        db.session.add(addSanpham)
        flash(f'{name} đã được thêm vào database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    
    return render_template('sanpham/addsp.html', form=form, title="Thêm sản phẩm", categories=categories)

