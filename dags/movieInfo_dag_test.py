# # unittest 모듈과 unittest.mock의 patch 기능을 임포트합니다.
# import unittest
# import movieInfo_dag
# from unittest.mock import patch

# # TestAirflowDAG 클래스를 정의하여 unittest.TestCase를 상속받습니다. 이 클래스는 테스트 케이스의 컨테이너 역할을 합니다.
# class TestAirflowDAG(unittest.TestCase):
#     # requests.get 함수를 패치하여 네트워크 호출 없이 테스트를 수행할 수 있게 합니다.
#     @patch('requests.get')
#     def test_fetch_data(self, mock_get):
#         # requests.get의 반환 값 설정. json 메소드가 호출되면 특정 데이터를 반환하도록 설정합니다.
#         mock_get.return_value.json.return_value = {'data': 'test data'}
#         # 실제 fetch_data 함수를 호출하여 데이터를 가져옵니다.
#         data = movieInfo_dag.fetch_data()
#         # fetch_data 함수가 반환한 데이터가 예상된 데이터와 일치하는지 검증합니다.
#         self.assertEqual(data, {'data': 'test data'})

#     # azure.storage.filedatalake.DataLakeServiceClient 클래스를 패치하여 실제 Azure 서비스 호출 없이 테스트합니다.
#     @patch('azure.storage.filedatalake.DataLakeServiceClient')
#     def test_save_to_data_lake(self, mock_service_client):
#         # DataLakeServiceClient의 메소드 체인을 모의 객체로 설정하여 각 메소드 호출을 가상으로 처리할 수 있습니다.
#         mock_client = mock_service_client.return_value.get_file_system_client.return_value.get_file_client.return_value
#         # 각 메소드 호출의 반환 값 설정. 여기서는 실제로는 아무 작업도 하지 않도록 설정합니다.
#         mock_client.create_file.return_value = None
#         mock_client.append_data.return_value = None
#         mock_client.flush_data.return_value = None
        
#         # save_to_data_lake 함수를 실행합니다. JSON 문자열 형태의 테스트 데이터를 제공합니다.
#         data = '{"test": "value"}'
#         save_to_data_lake(data)
        
#         # 각 메소드가 예상대로 한 번씩 호출되었는지 확인합니다.
#         mock_client.create_file.assert_called_once()
#         # append_data 메소드가 올바른 인자와 함께 호출되었는지 검증합니다.
#         mock_client.append_data.assert_called_once_with(data, 0, len(data))
#         # flush_data 메소드가 올바른 인자와 함께 호출되었는지 검증합니다.
#         mock_client.flush_data.assert_called_once_with(len(data))

# # 이 파일이 직접 실행될 때만 테스트가 실행되도록 합니다.
# if __name__ == '__main__':
#     unittest.main()
