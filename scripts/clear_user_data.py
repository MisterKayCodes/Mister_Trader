import sys
import os
import argparse

# Rule 11: Add parent directory to path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.user import User
from app.models.trade import Trade
from app.models.strategy import Strategy
from app.models.trading_plan import TradingPlan
from app.models.activity import Activity
from app.models.voice_note import VoiceNote
from app.models.trade_media import TradeMedia
from app.models.trade_psychology import TradePsychology
from app.models.user_stats import UserStats

def clear_user_data(identifier: str):
    db = SessionLocal()
    try:
        # Rule 1: Ensure we are operating on a known user state
        # Try searching by Telegram ID first
        user = db.query(User).filter(User.telegram_user_id == int(identifier) if identifier.isdigit() else False).first()
        
        if not user:
            print(f"\n❌ Error: User with ID/TG '{identifier}' not found in database.\n")
            return

        print(f"\n🗑️  Clearing records for user ID: {user.id} (TG: {user.telegram_user_id})...\n")

        # 1. Delete physical files from disk (Rule 2: Cleanup durable storage)
        media_files = db.query(TradeMedia).filter(TradeMedia.user_id == user.id).all()
        for media in media_files:
            if media.file_path and os.path.exists(media.file_path):
                try:
                    os.remove(media.file_path)
                    print(f"  ✅ Deleted media: {media.file_path}")
                except Exception as e:
                    print(f"  ⚠️  Failed to delete media file {media.file_path}: {e}")

        voice_files = db.query(VoiceNote).filter(VoiceNote.user_id == user.id).all()
        for voice in voice_files:
            if voice.file_path and os.path.exists(voice.file_path):
                try:
                    os.remove(voice.file_path)
                    print(f"  ✅ Deleted voice note: {voice.file_path}")
                except Exception as e:
                    print(f"  ⚠️  Failed to delete voice file {voice.file_path}: {e}")

        # 2. Delete DB records
        # We delete in order of dependencies (though PRAGMA foreign_keys=ON is now enabled)
        print("\n⏳ Wiping database records...")
        
        # Delete psychology entries linked to user's trades
        db.query(TradePsychology).filter(TradePsychology.trade_id.in_(
            db.query(Trade.id).filter(Trade.user_id == user.id)
        )).delete(synchronize_session=False)
        
        db.query(TradeMedia).filter(TradeMedia.user_id == user.id).delete()
        db.query(VoiceNote).filter(VoiceNote.user_id == user.id).delete()
        db.query(Trade).filter(Trade.user_id == user.id).delete()
        db.query(TradingPlan).filter(TradingPlan.user_id == user.id).delete()
        db.query(Strategy).filter(Strategy.user_id == user.id).delete()
        db.query(Activity).filter(Activity.user_id == user.id).delete()
        
        # Reset or Delete Stats
        stats = db.query(UserStats).filter(UserStats.user_id == user.id).first()
        if stats:
            db.delete(stats)

        db.commit()
        print(f"\n✨ Successfully cleared all trade records, media, and stats for TG ID '{user.telegram_user_id}'.")
        print("💡 Your account and PIN have been preserved. You can now start with fresh data.\n")

    except Exception as e:
        db.rollback()
        print(f"\n💥 An error occurred during wipe: {e}\n")
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wipe all trade data for a specific user.")
    parser.add_argument("identifier", help="Telegram ID of the user to clear")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    clear_user_data(args.identifier)
