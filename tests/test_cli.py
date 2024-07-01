import argparse
import builtins
import io
import os
import sys
from unittest import mock

from exitstatus import ExitStatus
import pytest

from cryptosteganography import cli
from cryptosteganography.utils import get_output_image_filename

INPUT_IMAGE = 'tests/assets/test_image.jpg'
INPUT_MESSAGE_TEXT_FILE = 'tests/assets/test_file1.txt'
INPUT_MESSAGE_TEXT_EMPTY_FILE = 'tests/assets/test_file2.txt'
INPUT_MESSAGE_AUDIO_FILE = 'tests/assets/test_file.mp3'
OUTPUT_IMAGE = 'tests/output_files/image_file_cli.png'
OUTPUT_IMAGE_JPG_EXPECTED = 'tests/output_files/image_file_cli_other.jpg'
OUTPUT_MESSAGE_FILE = 'tests/output_files/message_file_cli.txt'
OUTPUT_MESSAGE_AUDIO_FILE = 'tests/output_files/test_file_cli.mp3'

# The cli change any change output format to PNG
OUTPUT_IMAGE_JPG_REAL = get_output_image_filename(OUTPUT_IMAGE_JPG_EXPECTED)


def patch_open(open_func, files):
    def open_patched(
        path,
        mode='r',
        buffering=-1,
        encoding=None,
        errors=None,
        newline=None,
        closefd=True,
        opener=None
    ):
        if 'w' in mode and not os.path.isfile(path):
            files.append(path)
        return open_func(
            path,
            mode=mode,
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener
        )
    return open_patched


@pytest.fixture()
def cleanup_files(monkeypatch):
    """
    Delete files created by the tests.
    """
    files = [
        'output.png',
        OUTPUT_IMAGE,
        OUTPUT_IMAGE_JPG_REAL,
        OUTPUT_MESSAGE_FILE,
        OUTPUT_MESSAGE_AUDIO_FILE
    ]
    monkeypatch.setattr(builtins, 'open', patch_open(builtins.open, files))
    monkeypatch.setattr(io, 'open', patch_open(io.open, files))
    yield
    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass


def test_init():
    with mock.patch.object(cli, 'main', return_value=42):
        with mock.patch.object(cli, '__name__', '__main__'):
            with mock.patch.object(cli.sys, 'exit') as mock_exit:
                cli.init()
                assert mock_exit.call_args[0][0] == 42


def test_argparse_input_empty():
    # calling with no arguments goes to look at sys.argv, which is our arguments to py.test.
    with pytest.raises((SystemExit, NotImplementedError)):
        cli.main()


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command=''
    )
)
def test_empty_command(mock_args, monkeypatch, capsys) -> None:
    """
    Test if show help when command is empty
    """
    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure

    output = str(capsys.readouterr().out)

    assert "usage: cryptosteganography [-h] [-v] {save,retrieve}" in output
    assert "Cryptosteganography is an application to save or retrieve an encrypted message" in output
    assert "-h, --help       show this help message and exit" in output
    assert "-v, --version    show program's version number and exit" in output


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='cdsdcs'
    )
)
def test_invalid_command(mock_args, monkeypatch, capsys) -> None:
    """
    Test if show help when command is invalid
    """
    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure

    output = str(capsys.readouterr().out)

    assert "usage: cryptosteganography [-h] [-v] {save,retrieve}" in output
    assert "Cryptosteganography is an application to save or retrieve an encrypted message" in output
    assert "-h, --help       show this help message and exit" in output
    assert "-v, --version    show program's version number and exit" in output


###############################
# Save - Message String Tests #
###############################

@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file=INPUT_IMAGE,
        output_image_file=OUTPUT_IMAGE,
        message='Hello World. 你好，世界!!!'
    )
)
def test_save_message_success(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '48dj_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.success

    output = str(capsys.readouterr().out)

    assert output == f'Output image {OUTPUT_IMAGE} saved with success\n'


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file=INPUT_IMAGE,
        output_image_file='',
        message='Hello World. 你好，世界!!!'
    )
)
def test_save_message_empty_output_success(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '48dj_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.success

    output = str(capsys.readouterr().out)

    assert output == 'Output image output.png saved with success\n'


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file='bablakjbla.png',
        output_image_file=OUTPUT_IMAGE,
        message='Hello. 你好，世界!!!'
    )
)
def test_save_message_input_image_file_not_found_error(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '48dj_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure

    output = str(capsys.readouterr().out)
    assert output == 'Failed: Input file bablakjbla.png not found.\n'


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file=INPUT_MESSAGE_TEXT_FILE,
        output_image_file=OUTPUT_IMAGE,
        message='Hello. 你好，世界!!!'
    )
)
def test_save_message_invalid_input_image_error(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '48dj_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file=INPUT_IMAGE,
        output_image_file=OUTPUT_IMAGE,
        message='',
        message_file=''
    )
)
def test_save_message_empty_message_error(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: 'uhf8hf838fuh')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure

    output = str(capsys.readouterr().out)
    assert output == "Failed: Message can't be empty\n"


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file=INPUT_IMAGE,
        output_image_file=OUTPUT_IMAGE,
        message='Hello World. 你好，世界!!!'
    )
)
def test_save_message_empty_password_error(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: ' ')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure

    output = str(capsys.readouterr().out)
    assert output == "Failed: Password can't be empty\n"


###################################
# Retrieve - Message String Tests #
###################################

@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='retrieve',
        input_image_file=OUTPUT_IMAGE,
        retrieved_file=None
    )
)
def test_retrieve_message_success(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '48dj_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.success

    output = str(capsys.readouterr().out)
    assert output == 'Hello World. 你好，世界!!!\n'


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='retrieve',
        input_image_file=OUTPUT_IMAGE,
        retrieved_file=OUTPUT_MESSAGE_FILE
    )
)
def test_retrieve_message_as_file_success(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '48dj_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.success

    output = str(capsys.readouterr().out)
    assert output == f'{OUTPUT_MESSAGE_FILE} saved with success\n'

    with open(OUTPUT_MESSAGE_FILE, 'rb') as f:
        message = f.read()
        assert message.decode('utf-8') == 'Hello World. 你好，世界!!!'


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='retrieve',
        input_image_file=OUTPUT_IMAGE,
        retrieved_file=None
    )
)
def test_retrieve_message_invalid_password(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: 'Wrong Password')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure

    output = str(capsys.readouterr().out)
    assert output == 'No valid data found\n'


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='retrieve',
        input_image_file='bablakjbla.png',
        retrieved_file=None
    )
)
def test_retrieve_message_input_image_file_not_found_error(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '48dj_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure

    output = str(capsys.readouterr().out)
    assert output == 'No valid data found\n'


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='retrieve',
        input_image_file=INPUT_MESSAGE_TEXT_FILE,
        retrieved_file=None
    )
)
def test_retrieve_message_invalid_input_image_error(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '48dj_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='retrieve',
        input_image_file=OUTPUT_IMAGE,
        retrieved_file=None
    )
)
def test_retrieve_message_empty_password_error(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: ' ')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure

    output = str(capsys.readouterr().out)
    assert output == "Failed: Password can't be empty\n"


#############################
# Save - Message File Tests #
#############################

@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file=INPUT_IMAGE,
        output_image_file=OUTPUT_IMAGE,
        message='',
        message_file=INPUT_MESSAGE_TEXT_FILE
    )
)
def test_save_message_file_success(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '7348hffbsd_33222_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.success

    output = str(capsys.readouterr().out)

    assert output == f'Output image {OUTPUT_IMAGE} saved with success\n'


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file=INPUT_IMAGE,
        output_image_file=OUTPUT_IMAGE,
        message='',
        message_file=INPUT_MESSAGE_AUDIO_FILE
    )
)
def test_save_message_audio_file_success(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '7348hffbsd_33222_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.success

    output = str(capsys.readouterr().out)

    assert output == f'Output image {OUTPUT_IMAGE} saved with success\n'

    assert os.path.isfile(INPUT_MESSAGE_AUDIO_FILE)


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file=INPUT_IMAGE,
        output_image_file=OUTPUT_IMAGE,
        message='',
        message_file='invalid file'
    )
)
def test_save_message_file_not_found_error(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '7348hffbsd_33222_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure

    output = str(capsys.readouterr().out)
    assert output == 'Failed: File invalid file not found.\n'


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file=INPUT_IMAGE,
        output_image_file=OUTPUT_IMAGE,
        message='',
        message_file=INPUT_MESSAGE_TEXT_EMPTY_FILE
    )
)
def test_save_message_file_empty_error(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '7348hffbsd_33222_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.failure

    output = str(capsys.readouterr().out)
    assert output == "Failed: Message file content can't be empty\n"


#################################
# Retrieve - Message File Tests #
#################################
@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='retrieve',
        input_image_file=OUTPUT_IMAGE,
        retrieved_file=OUTPUT_MESSAGE_AUDIO_FILE
    )
)
def test_retrieve_message_audio_file_success(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: '7348hffbsd_33222_你好，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.success

    output = str(capsys.readouterr().out)
    assert output == f'{OUTPUT_MESSAGE_AUDIO_FILE} saved with success\n'

    # Compare if original file is equal to retrieved file
    with open(OUTPUT_MESSAGE_AUDIO_FILE, 'rb') as audio_file:
        output_audio = audio_file.read()
        with open(INPUT_MESSAGE_AUDIO_FILE, 'rb') as original_audio_file:
            original_audio = original_audio_file.read()
            assert original_audio == output_audio


#######################################
# Save/Retrieve - JPG output expected #
#######################################
@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='save',
        input_image_file=INPUT_IMAGE,
        output_image_file=OUTPUT_IMAGE_JPG_EXPECTED,
        message='Hello World. 你好，世界!!!'
    )
)
def test_save_message_jpg_output_success(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: 'Test，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.success

    output = str(capsys.readouterr().out)

    # Note: The output format is png
    assert output == f'Output image {OUTPUT_IMAGE_JPG_REAL} saved with success\n'


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(
        command='retrieve',
        input_image_file=OUTPUT_IMAGE_JPG_REAL,
        retrieved_file=None
    )
)
def test_retrieve_message_jpg_success(mock_args, monkeypatch, capsys) -> None:
    # Password prompt
    monkeypatch.setattr('getpass.getpass', lambda prompt: 'Test，世界')

    # Call CLI
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(cli.main())
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == ExitStatus.success

    output = str(capsys.readouterr().out)
    assert output == 'Hello World. 你好，世界!!!\n'

