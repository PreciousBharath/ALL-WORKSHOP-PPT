const validVoterRecords = [
  { username: '123456789012', aadhaar: '123456789012', voterId: 'VOT-00149' },
  { username: '234567890123', aadhaar: '234567890123', voterId: 'VOT-00462' },
  { username: '345678901234', aadhaar: '345678901234', voterId: 'VOT-00813' },
  { username: '456789012345', aadhaar: '456789012345', voterId: 'VOT-01274' },
  { username: 'VOT-00149', aadhaar: '123456789012', voterId: 'VOT-00149' },
  { username: 'VOT-00462', aadhaar: '234567890123', voterId: 'VOT-00462' },
  { username: 'VOT-00813', aadhaar: '345678901234', voterId: 'VOT-00813' },
  { username: 'VOT-01274', aadhaar: '456789012345', voterId: 'VOT-01274' },
]

export function getVoterMatch({ username, aadhaar, voterId, registry = validVoterRecords }) {
  const normalizedUsername = (username ?? '').trim().replace(/\s+/g, '')
  const normalizedAadhaar = (aadhaar ?? '').trim().replace(/\s+/g, '')
  const normalizedVoterId = (voterId ?? '').trim().toUpperCase()

  if (!normalizedUsername || !normalizedAadhaar || !normalizedVoterId) {
    return null
  }

  const preferredMatches = registry.filter((record) => (
    record.aadhaar === normalizedAadhaar &&
    record.voterId === normalizedVoterId &&
    (record.username === normalizedUsername || record.voterId === normalizedUsername)
  ))

  if (preferredMatches.length > 0) {
    const exactUsernameMatch = preferredMatches.find((record) => record.username === normalizedUsername)
    return exactUsernameMatch ?? preferredMatches[0]
  }

  return registry.find((record) => (
    record.aadhaar === normalizedAadhaar &&
    record.voterId === normalizedVoterId &&
    (record.username === normalizedUsername || record.voterId === normalizedUsername || record.username === normalizedAadhaar)
  )) ?? null
}
