SIGN_IN_MUTATION = """
mutation SignIn($email: String!, $password: String!){
  signin(input: { email: $email, password: $password}){
    me {
    id,
    email,
    firstName,
    lastName
    }
  }
}
"""

SIGN_OUT_MUTATION = """
mutation SignIn($everywhere: Boolean!){
  signout(input: { everywhere: $everywhere}){
    message
  }
}
"""

SIGN_UP_MUTATION = """
mutation SignIn($email: String!, $password: String!, $lastName: String!, $firstName: String!){
  signup(input: { email: $email, password: $password, lastName: $lastName, firstName: $firstName}){
    me {
    id,
    email,
    firstName,
    lastName
    }
  }
}
"""
