import hashlib

from apps.documents.models import BlockchainRecord

from .hash_service import calculate_sha256


def create_blockchain_record(
    *,
    document_version,
):
    """
    Create a blockchain-style integrity record for a document version.

    For now this is a local mock implementation.
    Later it can be replaced with a real blockchain/Web3 service.
    """

    payload = (
        f"{document_version.document_id}:"
        f"{document_version.version_number}:"
        f"{document_version.sha256_hash}"
    )

    blockchain_hash = hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()

    return {
        "document_id": document_version.document_id,
        "version_id": document_version.id,
        "version_number": document_version.version_number,
        "document_hash": document_version.sha256_hash,
        "blockchain_hash": blockchain_hash,
        "status": "confirmed",
    }


def verify_blockchain_record(
    *,
    document_version,
):
    """
    Verify the physical document file against its blockchain record.
    """

    try:
        record = document_version.blockchain_record
    except BlockchainRecord.DoesNotExist:
        return {
            "verified": False,
            "status": "not_found",
            "message": "Blockchain record not found.",
        }

    # Recalculate SHA-256 from the actual physical file.
    current_hash = calculate_sha256(
        document_version.file
    )

    # Check whether the current file matches
    # the hash stored in the blockchain record.
    document_hash_matches = (
        current_hash == record.document_hash
    )

    # Recreate the expected blockchain hash.
    payload = (
        f"{document_version.document_id}:"
        f"{document_version.version_number}:"
        f"{current_hash}"
    )

    expected_blockchain_hash = hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()

    blockchain_hash_matches = (
        expected_blockchain_hash
        == record.blockchain_hash
    )

    if document_hash_matches and blockchain_hash_matches:
        return {
            "verified": True,
            "status": "verified",
            "message": "Document integrity verified successfully.",
            "document_hash": current_hash,
            "blockchain_hash": record.blockchain_hash,
        }

    return {
        "verified": False,
        "status": "tampered",
        "message": "Document integrity verification failed.",
        "document_hash": current_hash,
        "blockchain_hash": record.blockchain_hash,
    }