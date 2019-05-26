import React, { useState, useEffect, useRef } from 'react'
import { Flex, Text } from 'rebass'
import { get } from 'axios'
import Web3 from 'web3'

window.web3 = new Web3(window.web3.currentProvider)

const baseUrl = 'http://localhost:8888/getCardInfo?timestamp='
const COMPANY_ADDR = '0x203D66c9b5e91C475499EE6E307F90E1BE25e501'

const useInterval = (callback, delay) => {
  const savedCallback = useRef()

  useEffect(() => {
    savedCallback.current = callback
  }, [callback])

  useEffect(() => {
    if (delay !== null) {
      let id = setInterval(() => savedCallback.current(), delay)
      return () => clearInterval(id)
    }
  }, [delay])
}

export default props => {
  const [user, setUser] = useState({})

  useInterval(() => {
    ;(async () => {
      const {
        data: { result },
      } = await get(baseUrl + Math.floor(Date.now() / 1000))
      setUser(result)
      if (result.address !== user.address) {
        const op = x => (x.length < 64 ? op('0' + x) : x)
        const raw = await window.web3.eth.call({
          to: '0x203D66c9b5e91C475499EE6E307F90E1BE25e501',
          data: '0x6b7b44d7' + op(result.address.slice(2)),
        })
        const userDetail = window.web3.eth.abi.decodeParameters(
          ['bool', 'string', 'uint256'],
          raw,
        )
        console.log(userDetail)
      }
    })()
  }, 1000)

  return (
    <Flex flexDirection="column" alignItems="center">
      {!user.whiteListed && (
        <Flex
          justifyContent="center"
          alignItems="center"
          style={{ height: '100vh' }}
        >
          <Text fontWeight={600} fontSize={24}>
            Please insert student card
          </Text>
        </Flex>
      )}
      {user.whiteListed && (
        <Flex flexDirection="column" alignItems="center">
          {user.address}
        </Flex>
      )}
    </Flex>
  )
}
