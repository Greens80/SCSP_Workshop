import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
import { Router } from 'express';

const ALLOWED_EMAIL = 'leif.jackson@gmail.com';

passport.use(new GoogleStrategy(
  {
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: '/auth/callback',
  },
  (_accessToken, _refreshToken, profile, done) => {
    const email = profile.emails?.[0]?.value;
    if (email !== ALLOWED_EMAIL) {
      return done(null, false, { message: 'Email not authorized.' });
    }
    return done(null, { id: profile.id, email, name: profile.displayName });
  }
));

passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((user, done) => done(null, user));

export const router = Router();

router.get('/google', passport.authenticate('google', { scope: ['email', 'profile'] }));

router.get(
  '/callback',
  passport.authenticate('google', { failureRedirect: '/auth/denied' }),
  (_req, res) => res.redirect('/')
);

router.get('/denied', (_req, res) => {
  res.status(403).send('<h1>Access denied</h1><p>Your Google account is not authorized to use this app.</p>');
});

router.get('/logout', (req, res, next) => {
  req.logout((err) => {
    if (err) return next(err);
    req.session.destroy(() => res.redirect('/auth/google'));
  });
});
