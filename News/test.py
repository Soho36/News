string = ('В качестве результата задания подготовьте файл, '
          'в котором напишете список всех команд, запускаемых в Django shell.')


def joined(strr):
    result = strr[:5] + ' ...'

    return result


result2 = joined(string)

print(result2)


# dd = list(string)
# dd.append('...')
# print(dd)