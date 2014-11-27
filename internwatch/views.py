from flask import render_template, redirect, url_for, flash, request

from internwatch.models import db, Posting
from internwatch.forms import ConfirmSendEmail

def register_routes(app):

  @app.route('/', methods=['GET'])
  def index():
    if request.args.get('show') == 'all':
      postings = Posting.query.all()
    else:
      postings = Posting.pending().all()
    return render_template('index.html', postings=postings)

  @app.route('/posting/<posting_id>', methods=['GET', 'POST'])
  def posting(posting_id):
    posting = Posting.query.filter_by(id=posting_id).first_or_404()
    email_response = posting.email_response_form
    if email_response.validate_on_submit():
      email_response.populate_obj(posting)

      if db.session.is_modified(posting):
        db.session.add(posting)
        db.session.commit()
        flash("Changes saved!")

      if request.form.get('send_email'):
        return redirect(url_for('send_email', posting_id=posting.id))

    if email_response.errors:
      flash("Could not save, check errors")

    return render_template('posting.html', posting=posting,
                           email_response=email_response)

  @app.route('/posting/<posting_id>/ignore', methods=['POST'])
  def ignore_posting(posting_id):
    posting = Posting.query.filter_by(id=posting_id).first_or_404()
    posting.ignore()
    db.session.add(posting)
    db.session.commit()
    return redirect(url_for('index'))

  @app.route('/posting/<posting_id>/send_email', methods=['GET', 'POST'])
  def send_email(posting_id):
    posting = Posting.query.filter_by(id=posting_id).first_or_404()
    form = ConfirmSendEmail()
    if form.validate_on_submit():
      if request.form.get('yes'):
        posting.send_email()
        db.session.add(posting)
        db.session.commit()
        flash('Email sent!')
      return redirect(url_for('posting', posting_id=posting_id))
    return render_template('confirm_send_email.html', posting=posting, form=form)
