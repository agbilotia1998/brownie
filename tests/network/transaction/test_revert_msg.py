#!/usr/bin/python3

import pytest

from brownie.exceptions import VirtualMachineError


def test_revert_msg_via_jump(ext_tester, console_mode):
    tx = ext_tester.getCalled(2)
    assert tx.revert_msg == "dev: should jump to a revert"


def test_revert_msg(evmtester, console_mode):
    tx = evmtester.revertStrings(0)
    assert tx.revert_msg == "zero"
    tx = evmtester.revertStrings(1)
    assert tx.revert_msg == "dev: one"
    tx = evmtester.revertStrings(2)
    assert tx.revert_msg == "two"
    tx = evmtester.revertStrings(3)
    assert tx.revert_msg == ""
    tx = evmtester.revertStrings(31337)
    assert tx.revert_msg == "dev: great job"


def test_nonpayable(tester, evmtester, console_mode):
    tx = evmtester.revertStrings(0, {"value": 100})
    assert tx.revert_msg == "Cannot send ether to nonpayable function"
    tx = tester.doNothing({"value": 100})
    assert tx.revert_msg == "Cannot send ether to nonpayable function"


def test_invalid_opcodes(evmtester):
    with pytest.raises(VirtualMachineError) as exc:
        evmtester.invalidOpcodes(0, 0)
    assert exc.value.revert_msg == "invalid opcode"
    with pytest.raises(VirtualMachineError) as exc:
        evmtester.invalidOpcodes(1, 1)
    assert exc.value.revert_msg == "dev: foobar"
    with pytest.raises(VirtualMachineError) as exc:
        evmtester.invalidOpcodes(3, 3)
    assert exc.value.revert_msg == "Index out of range"
