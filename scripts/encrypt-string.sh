#! /bin/bash

# 功能：加密字符串
# 参数 1：字段名
# 参数 2：被加密的字符串
ansible-vault encrypt_string --vault-password-file vault-password -n "${@:1}"
