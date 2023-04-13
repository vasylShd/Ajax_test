import pytest
from unittest.mock import patch
from unittest import mock
from scanner_handler import CheckQr

'''
Кейси для покриття тестами:
CASE_1 -- Необхідно просканувати QR-коди різної довжини, які є в БД і перевірити, чи програма
          призначає правильний колір залежно від довжини QR-коду.
CASE_2 -- Негативний кейс, в якому ми скануємо QR-код для довжини якого немає кольору
CASE_3 -- Перевірити сканування QR, якого немає БД.
CASE_4 -- Написати тести для випадку не успішного сканування та перевірити, що метод
          send_error був викликаний з потрібними аргументами.
CASE_5 -- Написати тести для успішного сканування і перевірити, що метод can_add_device
          повертає повідомлення у разі успішного сканування, за аналогією з тестом для
          send_error.
'''


class TestCheckQr:
    def new_database(self, qr_code:str):
        if qr_code in ['aaa', 'aaaaa', 'aaaaaaa']:
            return True
        else:
            return None

    def test_check_scanned_device(self, monkeypatch):
        check_qr = CheckQr()
        check_qr.check_in_db = mock.Mock(side_effect=self.new_database)

        # CASE_1
        qr_colors_dict = {'aaa': 'Red',
                          'aaaaa': 'Green',
                          'aaaaaaa': 'Fuzzy Wuzzy'}
        for qr, color in qr_colors_dict.items():
            check_qr.check_scanned_device(qr)
            assert check_qr.color == color

        # CASE_2
        qr = 'aaaa'
        with patch.object(check_qr, 'send_error') as mock_can_add_device:
            check_qr.check_scanned_device(qr)
            mock_can_add_device.assert_called_once_with(f"Error: Wrong qr length {len(qr)}")

        # CASE_3
        qr = 'aab'
        with patch.object(check_qr, 'send_error') as mock_send_error:
            check_qr.check_scanned_device(qr)
            mock_send_error.assert_called_once_with("Not in DB")

        # CASE_4
        qr_error_dict = {'aabba': 'Not in DB',
                         'aaaa': 'Error: Wrong qr length 4'}
        for qr, call in qr_error_dict.items():
            with patch.object(check_qr, 'send_error') as mock_send_error:
                check_qr.check_scanned_device(qr)
                mock_send_error.assert_called_once_with(call)

        # CASE_5
        qr = 'aaa'
        with patch.object(check_qr, 'can_add_device') as mock_can_add_device:
            check_qr.check_scanned_device(qr)
            mock_can_add_device.assert_called_once_with(f'hallelujah {qr}')
