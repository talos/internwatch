def register_routes(app):

  @app.route('/', methods=['GET'])
  def index(cls):
    pass

  @app.route('/posting/<id>', methods=['GET', 'POST'])
  def posting(cls, **kwargs):
    pass

  @app.route('/posting/<id>/send_email', methods=['POST'])
  def send_email(cls, posting_id):
    pass
