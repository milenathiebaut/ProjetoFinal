import re
from typing import Any


def add_error(self_name: str, msg: str, errors: dict) -> bool:
    if errors.get(self_name) is None:
        errors[self_name] = []
    errors[self_name].append(msg)


def is_in_range(
    self: int, self_name: str, low: int, high: int, errors: dict
) -> bool:
    if low <= self <= high:
        return True
    else:
        add_error(
            self_name, f"O valor deste campo deve estar entre {low} e {high}.", errors
        )
        return False


def is_not_none(self: Any, self_name: str, errors: dict) -> bool:
    if self is not None:
        return True
    else:
        add_error(self_name, f"O valor deste campo não pode ser nulo.", errors)
        return False


def is_not_empty(self: str, self_name: str, errors: dict) -> bool:
    if self.strip() != "":
        return True
    else:
        add_error(self_name, f"O valor deste campo não pode ser vazio.", errors)
        return False


def is_size_between(
    self: str, self_name: str, min_size: int, max_size: int, errors: dict
) -> bool:
    if min_size <= len(self) <= max_size:
        return True
    else:
        add_error(
            self_name,
            f"Este campo deve ter entre {min_size} e {max_size} caracteres.",
            errors,
        )
        return False


def is_max_size(self: str, self_name: str, max_size: int, errors: dict) -> bool:
    if len(self) <= max_size:
        return True
    else:
        add_error(
            self_name, f"Este campo deve ter no máximo {max_size} caracteres.", errors
        )
        return False


def is_min_size(self: str, self_name: str, min_size: int, errors: dict) -> bool:
    if len(self) >= min_size:
        return True
    else:
        add_error(
            self_name, f"Este campo deve ter no mínimo {min_size} caracteres.", errors
        )
        return False


def is_matching_regex(self: str, self_name: str, regex: str, errors: dict) -> bool:
    if re.match(regex, self) is not None:
        return True
    else:
        add_error(
            self_name, "O valor deste campo está com o formato incorreto.", errors
        )
        return False


def is_email(self: str, self_name: str, errors: dict) -> bool:
    if (
        re.match(
            r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
            self,
        )
        is not None
    ):
        return True
    else:
        add_error(
            self_name,
            "O valor deste campo deve ser um e-mail com formato válido.",
            errors,
        )
        return False


def is_cpf(self: str, self_name: str, errors: dict) -> bool:
    if re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", self) is not None:
        return True
    else:
        add_error(self_name, "O valor deste campo deve ser um CPF válido.", errors)
        return False


def is_cnpj(self: str, self_name: str, errors: dict) -> bool:
    if re.match(r"^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$", self) is not None:
        return True
    else:
        add_error(self_name, "O valor deste campo deve ser um CNPJ válido.", errors)
        return False


def is_phone_number(self: str, self_name: str, errors: dict) -> bool:
    if re.match(r"^\(\d{2}\)\d{4,5}-\d{4}$", self) is not None:
        return True
    else:
        add_error(
            self_name, "O valor deste campo deve ser um telefone válido.", errors
        )
        return False


def is_cep(self: str, self_name: str, errors: dict) -> bool:
    if re.match(r"^\d{5}-\d{3}$", self) is not None:
        return True
    else:
        add_error(self_name, "O valor deste campo deve ser um CEP válido.", errors)
        return False


def is_person_name(self: str, self_name: str, errors: dict) -> bool:
    if re.match(r"^[a-zA-ZÀ-ú']{2,40}$", self) is not None:
        return True
    else:
        add_error(self_name, "O valor deste campo deve ser um nome válido.", errors)
        return False


def is_person_fullname(self: str, self_name: str, errors: dict) -> bool:
    if re.match(r"^[a-zA-ZÀ-ú']{2,40}(?:\s[a-zA-ZÀ-ú']{2,40})+$", self) is not None:
        return True
    else:
        add_error(self_name, "O valor deste campo deve ser um nome completo válido.", errors)
        return False
    
    
def is_project_name(self: str, self_name: str, errors: dict) -> bool:
    if re.match(r"^[\w]+(\s[\w]+)*$", self) is not None:
        return True
    else:
        add_error(self_name, "O valor deste campo deve ser um nome válido.", errors)
        return False


def is_password(self: str, self_name: str, errors: dict) -> bool:
    """
    Tenha pelo menos um caractere minúsculo.
    Tenha pelo menos um caractere maiúsculo.
    Tenha pelo menos um dígito.
    Tenha pelo menos um caractere especial dentre os especificados (@$!%*?&).
    Tenha um comprimento de pelo menos 4 e no máximo 64 caracteres.
    """
    if (
        re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{4,64}$",
            self,
        )
        is not None
    ):
        return True
    else:
        add_error(
            self_name,
            "O valor deste campo deve ser uma senha válida entre 4 e 64 caracteres, contendo caracteres maiúsculos, minúsculos, dígitos e caracteres especiais (@$!%*?&).",
            errors,
        )
        return False


def is_matching_fields(
    self: str,
    self_name: str,
    matching_field: str,
    matching_field_label: str,
    errors: dict,
) -> bool:
    if self.strip() == matching_field.strip():
        return True
    else:
        add_error(
            self_name,
            f"O valor deste campo deve ser igual ao do campo {matching_field_label}.",
            errors,
        )
        return False


def is_greater_than(
    self: int, self_name: str, value: int, errors: dict
) -> bool:
    if self > value:
        return True
    else:
        add_error(self_name, f"O valor deste campo deve ser maior que {value}.", errors)
        return False


def is_selected_id_valid(self: int, self_name: str, errors: dict) -> bool:
    if self > 0:
        return True
    else:
        add_error(self_name, f"Selecione uma opção para este campo.", errors)
        return False


def is_less_than(
    self: int, self_name: str, value: int, errors: dict
) -> bool:
    if self < value:
        return True
    else:
        add_error(self_name, f"O valor deste campo deve ser menor que {value}.", errors)
        return False


def is_greater_than_or_equal(
    self: int, self_name: str, value: int, errors: dict
) -> bool:
    if self >= value:
        return True
    else:
        add_error(
            self_name, f"O valor deste campo deve ser maior ou igual a {value}.", errors
        )
        return False


def is_less_than_or_equal(
    self: int, self_name: str, value: int, errors: dict
) -> bool:
    if self <= value:
        return True
    else:
        add_error(
            self_name, f"O valor deste campo deve ser menor ou igual a {value}.", errors
        )
        return False
