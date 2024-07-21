import ansible.parsing.vault as ansible_vault


def is_encrypted(data):
    return ansible_vault.is_encrypted(data)


class FileSecret(ansible_vault.VaultSecret):
    def __init__(self, path: str):
        with open(path, "rb") as f:
            _bytes = f.read()
        super().__init__(_bytes)


class Vault:
    def __init__(self, secret_file: str = "vault-password") -> None:
        self.cipher = ansible_vault.VaultAES256()
        self.cipher_name = "AES256"

        self.secret = FileSecret(secret_file)

    def encrypt(self, text: str):
        b_plaintext = text.encode("utf-8")
        b_ciphertext = self.cipher.encrypt(b_plaintext, self.secret)
        b_vaulttext = ansible_vault.format_vaulttext_envelope(
            b_ciphertext, self.cipher_name
        )
        return b_vaulttext.decode("utf-8")

    def decrypt(self, text: str):
        b_vaulttext_envelope = text.encode("utf-8")
        b_ciphertext, b_version, cipher_name, vault_id = (
            ansible_vault.parse_vaulttext_envelope(b_vaulttext_envelope)
        )
        # TODO: get cipher by cipher_name
        b_plaintext = self.cipher.decrypt(b_ciphertext, self.secret)
        return b_plaintext.decode("utf-8")
