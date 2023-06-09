from app import db
from cert.repos import SQLCertificateRepo
from group.repos import SQLGroupRepo
from cert.usecases import CertificateUC
from group.usecases import GroupUC

group_repo = SQLGroupRepo(db=db)
group_uc = GroupUC(repo=group_repo)

cert_repo = SQLCertificateRepo(db=db, group_repo=group_repo)
cert_uc = CertificateUC(repo=cert_repo, group_uc=group_uc)
