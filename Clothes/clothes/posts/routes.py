from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from clothes import db
from clothes.models import Post
from clothes.posts.forms import PostForm, SearchForm

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.about'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post',form1 = SearchForm())

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post,form1 = SearchForm())

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.about', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post',form1 = SearchForm())

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.about'))

@posts.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@posts.route("/search", methods=['POST'])
def search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        post_searched = form.searched.data
        page = request.args.get('page', 1, type = int)
        posts = posts.filter(Post.content.like('%' + post_searched + '%')).order_by(Post.date_posted.desc())\
        .paginate(per_page=100)
        #posts = posts.order_by(Post.title).all()

        return render_template("search.html", form=form, searched=post_searched, posts=posts,form1 = SearchForm(), title='Search')