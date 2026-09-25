const router = require('express').Router();
const { githubCallback, verifyUser } = require('../Controllers/AuthController');

/**
 * @swagger
 * /api/auth/github:
 *   get:
 *     description: Redirects the user to GitHub for OAuth authentication.
 *     responses:
 *       302:
 *         description: Redirect to GitHub OAuth
 */
router.get('/github', (req, res) => {
    const clientId = process.env.GITHUB_CLIENT_ID?.trim();

    if (!clientId || clientId.startsWith('your-')) {
        return res.status(503).json({
            error: 'GitHub OAuth is not configured',
            message: 'Set GITHUB_CLIENT_ID in the server environment before signing in.'
        });
    }

    const githubAuthUrl = new URL('https://github.com/login/oauth/authorize');
    githubAuthUrl.searchParams.set('client_id', clientId);
    githubAuthUrl.searchParams.set('scope', 'user:email');
    res.redirect(githubAuthUrl.toString());
});

/**
 * @swagger
 * /api/auth/github/callback:
 *   get:
 *     description: Handles the callback from GitHub after OAuth authentication.
 *     responses:
 *       302:
 *         description: Redirect to Home after Login
 *       400:
 *         description: Error: No authorization code received.
 *       500:
 *         description: Error: Could not retrieve access token.
 */
router.get('/github/callback', githubCallback);

/**
 * @swagger
 * /api/auth/verifyUser:
 *   post:
 *     description: Verifies the user token for the frontend.
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *     responses:
 *       200:
 *         description: User verified
 */
router.post('/verifyUser', verifyUser);

/**
 * @swagger
 * /api/auth/logout:
 *   post:
 *     description: Clears the user token & Logs out the user.
 *     responses:
 *       200:
 *         description: Logged out Successfully.
 *       500:
 *         description: Logout failed.
 */
router.post('/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) return res.status(500).json({ message: 'Logout failed' });
        res.clearCookie('token');
        res.json({ status: true });
    });
});


module.exports = router;