from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def get_callback_url(self):
        return url_for('oath_callback', provider=self.provider_name, _external=True)

    @classmethod
    def get_provier(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSingIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response='code',
            redirect_url=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}
        )
        me = oauth_session.get('me?fields=id,email').json()
        return (
            'facebook$' + me['id'],
            me.get('email').split('@')[0],
            me.get('email') # Facebook doesn't provide username
        )

class TwitterSignIn(OAuthSignIn):
    def __init__(self):
        super(TwitterSignIn, self).__init__('twiiter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )

        def authorize(self):
            request_tken = self.service.get_request_token(
                params={'oauth_callbac': self.get_callback_url()}
            )
            session['request_token'] = request_token
            return redirect(self.service.get_authorize_url(request_token[0]))        

        def callback(self):
            request_token = session.pop('request_token')
            if 'oauth_verified' not in request.args:
                return None, None, None
            oauth_session = self.service.get_auth_session(
                request_token[0],
                request_token[1],
                data={'oauth_verified': request.args['oauth_verifier']}
            )
            me = oauth_sessions.get('account/verify_credentials.json').json()
            social_id = 'twitter$' + str(me.get('id'))
            username = me.get('screen_name')
            return social_id, username, None # Twitter does not provide email
