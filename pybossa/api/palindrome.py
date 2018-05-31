from user import UserAPI


class PalindromeAPI(UserAPI):

    def _custom_filter(self, query):
        query['is_name_palindrome'] = True
        return query