from market import app, db
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():

    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase
        purchased_item = request.form.get('purchased_item')
        p_item_obj = Item.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                p_item_obj.buy(current_user)
                flash(
                    f"Congratulation for your purchase of {p_item_obj.price}", category='success')
            else:
                flash(
                    f"You don't have enough money to purchase {p_item_obj.name}. It miss {p_item_obj.price - current_user.budget}", category='danger')

        # Sell
        sold_item = request.form.get('sold_item')
        s_item_obj = Item.query.filter_by(name=sold_item).first()
        if s_item_obj:
            if current_user.can_sell(s_item_obj):
                s_item_obj.sell(current_user)
                flash(
                    f"Congratulation, you sold {s_item_obj.price}", category='success')
            else:
                flash(
                    f"You can't sell {s_item_obj.name}.", category='danger')

        return redirect(url_for('market_page'))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, owned_items=owned_items, purchase_form=purchase_form, selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f'Account created, you are log in as : {user_to_create.username}', category='success')

        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_mess in form.errors.values():
            flash(f'There was an error : {err_mess}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                form.password.data):
            login_user(attempted_user)
            flash(
                f'You are log in as : {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash(f'Username and password does not match', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))
