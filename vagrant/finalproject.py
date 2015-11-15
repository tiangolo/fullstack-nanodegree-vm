from flask import Flask, render_template, url_for, request, redirect, jsonify, flash, get_flashed_messages
from finaldb import *
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
session = sessionmaker(engine)()


#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}



@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify({'Restaurants': [restaurant.serialize for restaurant in restaurants]})


@app.route('/restaurant/new', methods=['POST', 'GET'])
def newRestaurant():
    if request.method == 'GET':
        return render_template('newrestaurant.html')
    elif request.method == 'POST':
        if request.form['name']:
            use_restaurant = Restaurant(name=request.form['name'])
            session.add(use_restaurant)
            session.commit()
            flash('New restaurant %s created' % use_restaurant.name)
            return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if request.method == 'GET':
        return render_template('editrestaurant.html', restaurant_id=restaurant.id, restaurant=restaurant)
    elif request.method == 'POST':
        if request.form['name']:
            restaurant.name = request.form['name']
            session.add(restaurant)
            session.commit()
            flash('Restaurant %s successfully edited' % restaurant.name)
            return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if request.method == 'GET':
        return render_template('deleterestaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)
    elif request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('Restaurant %s successfully deleted' % restaurant.name)
        return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify({'MenuItems': [item.serialize for item in items]})


@app.route('/restaurant/<int:restaurant_id>/menu/<int:item_id>/JSON')
def showItemJSON(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).first()
    return jsonify({'MenuItem': item.serialize})


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newitem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newitem)
        session.commit()
        flash('New menu item %s successfully created' % newitem.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        session.add(item)
        session.commit()
        flash('Menu item %s successfully edited' % item.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    if request.method == 'GET':
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'GET':
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item)
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Menu item %s successfully deleted' % item.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))




if __name__ == '__main__':
    app.secret_key = 'asdfasdf'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)