import re
with open('backend/tests/api/v1/test_transcripts.py', 'r') as f:
    text = f.read()

text = re.sub(
    r'class MockSource:\s*id = source_id\s*project_id = project_id\s*has_audio = (True|False)\s*local_storage_reference = \"/tmp/test.mp4\"\s*mock_db = MagicMock\(\)\s*mock_result = MagicMock\(\)\s*mock_result.scalars\(\).first.return_value = MockSource\(\)',
    r'''mock_source = MagicMock()
        mock_source.id = source_id
        mock_source.project_id = project_id
        mock_source.has_audio = \1
        mock_source.local_storage_reference = "/tmp/test.mp4"
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars().first.return_value = mock_source''',
    text
)

text = re.sub(
    r'class MockSource:\s*id = source_id\s*project_id = project_id\s*mock_db = MagicMock\(\)\s*mock_result = MagicMock\(\)\s*mock_result.scalars\(\).first.return_value = MockSource\(\)',
    r'''mock_source = MagicMock()
        mock_source.id = source_id
        mock_source.project_id = project_id
        mock_db = MagicMock()
        mock_result = MagicMock()
        mock_result.scalars().first.return_value = mock_source''',
    text
)

with open('backend/tests/api/v1/test_transcripts.py', 'w') as f:
    f.write(text)
