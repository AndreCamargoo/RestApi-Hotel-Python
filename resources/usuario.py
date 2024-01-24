from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from secrets import compare_digest
from blacklist import BLACKLIST

argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help="This field 'login' cannot be left blank.")
argumentos.add_argument('senha', type=str, required=True, help="This field 'senha' cannot be left blank.")

class User(Resource):    
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404 # not found  
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An error ocurred trying delete user.'}, 500 # Internal Server Error
            
            return {'message': 'User deleted.'}, 200
        return {'message': 'User not found.'}, 404
    
class UserRegister(Resource):    
    def post(self):               
        dados = argumentos.parse_args()
        
        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}
        
        user = UserModel(**dados)
        try:
            user.save_user()
        except:
            return {'message': 'An internal error ocurred trying to save user.'}, 500 # Internal Server Error
        
        return {'message': 'User created successfully!'}, 201 # Created
    
class UserLogin(Resource):    
    @classmethod
    def post(cls):
        dados = argumentos.parse_args()
        
        user = UserModel.find_by_login(dados['login'])
        if user and compare_digest(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200
        return {'message': 'The username or password is incorrect.'}, 401 # Unauthorized
    
class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200