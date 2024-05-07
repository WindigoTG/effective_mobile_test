from wallet.wallet_handler import WalletHandler


def main():
    wallet_handler = WalletHandler("data/wallet.json")
    wallet_handler.run()


if __name__ == '__main__':
    main()
