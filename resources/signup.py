from flask_restful import Resource, reqparse

from models.user import UserModel
from models.clinic import ClinicModel

def parse_request():
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('clinic', type=dict, help='This field cannot be blank', required=True)
    request_parser.add_argument('fullname', help='This field cannot be blank', required=True)
    request_parser.add_argument('email', help='This field cannot be blank', required=True)
    request_parser.add_argument('password', help='This field cannot be blank', required=True)
    return request_parser.parse_args()

def validate_signup(request_args):
    clinic_cnpj = request_args.get('clinic').get('cnpj')
    clinic_description = request_args.get('clinic').get('description')
    user_email = request_args.get('email')
    user_fullname = request_args.get('fullname')
    user_password = request_args.get('password')
    if (clinic_cnpj is None) or (clinic_cnpj == ''):
        return (False, ({ 'status': 'error', 'message': 'Informe o CPF/CNPJ da Clínica.', 'field': 'clinic.cnpj'}, 400))
    elif ClinicModel.find_by_cnpj(clinic_cnpj) is not None:
        return (False, ({ 'status': 'error', 'message': 'Este CPF/CNPJ já está cadastrado.', 'field': 'clinic.cnpj'}, 400))
    if (clinic_description is None) or (clinic_description == ''):
        return (False, ({ 'status': 'error', 'message': 'Informe o Nome da Clínica.', 'field': 'clinic.description'}, 400))
    if (user_email is None) or (user_email == ''):
        return (False, ({ 'status': 'error', 'message': 'Informe o seu Email.', 'field': 'email'}, 400))
    elif UserModel.find_by_email(user_email) is not None:
        return (False, ({ 'status': 'error', 'message': 'Este email já está cadastrado.', 'field': 'email'}, 400))
    if (user_fullname is None) or (user_fullname == ''):
        return (False, ({ 'status': 'error', 'message': 'Informe o seu Nome Completo.', 'field': 'fullname'}, 400))
    if (user_password is None) or (user_password == '')  or (len(user_password) < 6):
        return (False, ({ 'status': 'error', 'message': 'Informe uma senha válida.', 'field': 'password'}, 400))
    return (True, None)


class SignUp(Resource):

    def post(self):
        request_args = parse_request()
        (valid, error_response) = validate_signup(request_args)
        if not valid:
            return error_response
        try:
            user_model = UserModel(
                email = request_args.get('email'), 
                fullname = request_args.get('fullname'),
                username = request_args.get('email'),
                password = UserModel.generate_hash(request_args.get('password')),
                clinic = ClinicModel(
                    cnpj = request_args.get('clinic').get('cnpj'),
                    description = request_args.get('clinic').get('description')
                )
            )
            user_model.save()
            return {'status': 'success', 'record': user_model.json()}
        except:
            return {'status': 'error'}
      
