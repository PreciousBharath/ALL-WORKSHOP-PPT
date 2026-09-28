import { describe, expect, it } from 'vitest'
import { getVoterMatch } from './voterValidation.js'

describe('getVoterMatch', () => {
  it('accepts a valid Aadhaar and Voter ID combination from the registry', () => {
    const match = getVoterMatch({
      username: 'VOT-00149',
      aadhaar: '123456789012',
      voterId: 'VOT-00149',
    })

    expect(match).toEqual({
      username: 'VOT-00149',
      aadhaar: '123456789012',
      voterId: 'VOT-00149',
    })
  })

  it('rejects a vote when the voter details do not match any registered record', () => {
    const match = getVoterMatch({
      username: 'VOT-00149',
      aadhaar: '999999999999',
      voterId: 'VOT-00200',
    })

    expect(match).toBeNull()
  })
})
