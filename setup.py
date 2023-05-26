from app import db
from repos_cert import SQLCertificateRepo
from repos_group import SQLGroupRepo
from usecases_cert import CertificateUC
from usecases_group import GroupUC

cert_repo = SQLCertificateRepo(db=db)
cert_uc = CertificateUC(repo=cert_repo)

group_repo = SQLGroupRepo(db=db)
group_uc = GroupUC(repo=group_repo)
