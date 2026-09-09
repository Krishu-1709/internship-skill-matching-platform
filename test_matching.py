from services.matching import calculate_match


student = ["Python", "Linux", "Networking", "SQL"]

internship = ["Python", "Linux", "Networking", "OWASP"]

result = calculate_match(student, internship)

print(result)