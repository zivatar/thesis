import unittest

from climate.classes.Gravatar import Gravatar

if __name__ == '__main__':
    unittest.main()


class GravatarTestCase(unittest.TestCase):
    def test_empty_email(self):
        self.assertTrue(
            Gravatar.get_gravatar_url(
                '') == 'https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?d=identicon&s=100' or
            Gravatar.get_gravatar_url(
                '') == 'https://www.gravatar.com/avatar/d41d8cd98f00b204e9800998ecf8427e?s=100&d=identicon'
        )

    def test_real_email_without_gravatar(self):
        self.assertTrue(
            Gravatar.get_gravatar_url('rendeles10@gmail.com') ==
            'https://www.gravatar.com/avatar/63f5e37aadce48600a133c88d4b89fe8?d=identicon&s=100' or
            Gravatar.get_gravatar_url('rendeles10@gmail.com') ==
            'https://www.gravatar.com/avatar/63f5e37aadce48600a133c88d4b89fe8?s=100&d=identicon'
        )

    def test_real_email_with_gravatar(self):
        self.assertTrue(
            Gravatar.get_gravatar_url('macgyver1024@gmail.com') ==
            'https://www.gravatar.com/avatar/58c594b1465ea0c8d93c8860dfb16a30?d=identicon&s=100' or
            Gravatar.get_gravatar_url('macgyver1024@gmail.com') ==
            'https://www.gravatar.com/avatar/58c594b1465ea0c8d93c8860dfb16a30?s=100&d=identicon'
        )

    def test_xl_size(self):
        self.assertTrue(
            Gravatar.get_gravatar_url('rendeles10@gmail.com', 512) ==
            'https://www.gravatar.com/avatar/63f5e37aadce48600a133c88d4b89fe8?d=identicon&s=512' or
            Gravatar.get_gravatar_url('rendeles10@gmail.com', 512) ==
            'https://www.gravatar.com/avatar/63f5e37aadce48600a133c88d4b89fe8?s=512&d=identicon'
        )
