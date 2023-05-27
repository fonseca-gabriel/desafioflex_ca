from app import db
from cert.repos import SQLCertificateRepo
from group.repos import SQLGroupRepo
from cert.usecases import CertificateUC
from group.usecases import GroupUC

cert_repo = SQLCertificateRepo(db=db)
cert_uc = CertificateUC(repo=cert_repo)

group_repo = SQLGroupRepo(db=db)
group_uc = GroupUC(repo=group_repo)
