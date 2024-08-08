#! /bin/bash

git_push_until_success() {
    while true; do
        git push
        if [ $? -eq 0 ]; then
            echo "Push 成功!"
            break
        else
            echo "Push 失败，即将重试"
        fi
    done
}

pushd modules/iapyc
git_push_until_success
popd

git_push_until_success
