require('dotenv').config();
const mongoose = require('mongoose');
const User = require('./models/User');

const email = process.argv[2];
const newPassword = process.argv[3];

async function main() {
  if (!process.env.MONGODB_URI) {
    console.error('Error: MONGODB_URI not found in .env');
    process.exit(1);
  }

  await mongoose.connect(process.env.MONGODB_URI);

  if (!email) {
    console.log('\n--- Registered Users in Database ---');
    const users = await User.find({}, 'name email createdAt').sort({ createdAt: -1 });
    users.forEach((u, i) => {
      console.log(`${i + 1}. Name: ${u.name} | Email: ${u.email} (Created: ${new Date(u.createdAt).toLocaleDateString()})`);
    });
    console.log('\nTo reset password, run:');
    console.log('  node reset-password.js <email> <newPassword>\n');
    process.exit(0);
  }

  if (!newPassword || newPassword.length < 6) {
    console.error('Error: Password must be at least 6 characters long.');
    console.log('Usage: node reset-password.js <email> <newPassword>');
    process.exit(1);
  }

  const user = await User.findOne({ email: email.toLowerCase().trim() });
  if (!user) {
    console.error(`User with email "${email}" not found.`);
    process.exit(1);
  }

  user.password = newPassword;
  await user.save();

  console.log(`\n✅ Password successfully updated for ${user.name} (${user.email})!`);
  console.log(`New password: ${newPassword}\n`);
  process.exit(0);
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
