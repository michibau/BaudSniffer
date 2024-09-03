from BaudSniffer import *
# in the test's setup code
from unittest import mock  # or just "import mock"
sys = mock.MagicMock()
sys.configure_mock(platform='Linux')
sys.platform 
'Linux'

main